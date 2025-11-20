import os
import psycopg2
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash
from dotenv import load_dotenv
from PIL import Image as PILImage
import io
import re
from collections import Counter

# Auth Imports
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# PDF Imports
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as PDFImage, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "super_secret_key_change_me") 

# --- CONFIGURATION ---
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# --- DATABASE HELPER ---
def get_db_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

# --- USER MODEL ---
class User(UserMixin):
    def __init__(self, id, username, is_admin=False):
        self.id = id
        self.username = username
        self.is_admin = is_admin

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, is_admin FROM users WHERE id = %s", (user_id,))
    user_data = cur.fetchone()
    cur.close()
    conn.close()
    if user_data:
        return User(id=user_data[0], username=user_data[1], is_admin=user_data[2])
    return None

# --- SYSTEM PROMPT ---
SYSTEM_PROMPT = """
You are MediSimplify. 
1. Analyze symptoms/images.
2. Explain in simple terms.
3. Suggest POSSIBLE causes (NO diagnosis).
4. Disclaimer: See a doctor.
5. Emergency: Call 911 if severe.
6. Tone: Professional, Teal, Calm.
7. Language: Detect and match user language.
"""
model = genai.GenerativeModel(model_name="gemini-2.5-flash-preview-09-2025", system_instruction=SYSTEM_PROMPT)

# --- AUTH ROUTES ---
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cur.fetchone():
            flash('Username already exists')
            return redirect(url_for('signup'))
            
        hashed_pw = generate_password_hash(password)
        cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_pw))
        conn.commit()
        cur.close()
        conn.close()
        
        flash('Account created! Please log in.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, username, password_hash, is_admin FROM users WHERE username = %s", (username,))
        user_data = cur.fetchone()
        cur.close()
        conn.close()
        
        if user_data and check_password_hash(user_data[2], password):
            user = User(id=user_data[0], username=user_data[1], is_admin=user_data[3])
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- APP ROUTES ---
@app.route('/')
@login_required
def index():
    return render_template('index.html', user=current_user)

@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return "Access Denied", 403
        
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM chat_logs")
    total_chats = cur.fetchone()[0]
    
    cur.execute("SELECT user_input FROM chat_logs ORDER BY timestamp DESC LIMIT 100")
    messages = [row[0] for row in cur.fetchall()]
    
    cur.close()
    conn.close()
    
    text_blob = " ".join(messages).lower()
    stopwords = set(['i', 'have', 'a', 'is', 'the', 'and', 'to', 'of', 'in', 'my', 'it', 'image', 'uploaded'])
    words = re.findall(r'\w+', text_blob)
    filtered_words = [w for w in words if w not in stopwords and len(w) > 3]
    common_keywords = Counter(filtered_words).most_common(5)
    
    return render_template('dashboard.html', total_users=total_users, total_chats=total_chats, keywords=common_keywords, user=current_user)

@app.route('/chat', methods=['POST'])
@login_required
def chat():
    user_message = request.form.get('message')
    session_id = request.form.get('session_id')
    image_file = request.files.get('image')

    if not user_message and not image_file:
        return jsonify({'error': 'No input provided'}), 400

    try:
        # Build History
        history = []
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_input, ai_response FROM chat_logs WHERE session_id = %s ORDER BY timestamp ASC LIMIT 5", (session_id,))
        rows = cur.fetchall()
        for row in rows:
             user_text = row[0].replace("[Image Uploaded] ", "")
             history.append({"role": "user", "parts": [user_text]})
             history.append({"role": "model", "parts": [row[1]]})
        
        current_parts = []
        if user_message: current_parts.append(user_message)
        
        has_image = False
        image_bytes = None
        
        if image_file:
            image_file.seek(0)
            image_bytes = image_file.read()
            image_file.seek(0)
            img = PILImage.open(image_file.stream)
            current_parts.append(img)
            has_image = True
            if not user_message: current_parts.append("Analyze this image.")

        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(current_parts)
        ai_text = response.text

        # Save to DB
        db_user_input = f"[Image Uploaded] {user_message}" if has_image else user_message
        cur.execute(
            "INSERT INTO chat_logs (session_id, user_input, ai_response, has_image, image_data, user_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (session_id, db_user_input, ai_text, has_image, psycopg2.Binary(image_bytes) if image_bytes else None, current_user.id)
        )
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'response': ai_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- HELPER: Markdown to PDF Flowables ---
def markdown_to_flowables(text, styles):
    """Parses Gemini Markdown into ReportLab Flowables (Tables, Bold, Headers)"""
    flowables = []
    lines = text.split('\n')
    in_table = False
    table_data = []
    
    # Styles
    normal_style = styles['Normal']
    normal_style.fontSize = 10
    normal_style.leading = 14
    
    # Style for Table Cells (Small font to fit)
    cell_style = ParagraphStyle('Cell', parent=normal_style, fontSize=9, leading=11)
    
    # List Style
    bullet_style = ParagraphStyle('Bullet', parent=normal_style, leftIndent=15, firstLineIndent=0, spaceAfter=2)

    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # --- TABLE DETECTION ---
        if line.startswith('|'):
            # It's a table row
            if '---' in line: continue # Skip separator lines like |---|---|
            
            # Extract cells: | A | B | -> ['A', 'B']
            cells = [c.strip() for c in line.strip('|').split('|')]
            
            # Wrap text in Paragraphs so it wraps inside the table cell
            row_cells = [Paragraph(cell, cell_style) for cell in cells]
            
            if not in_table:
                in_table = True
                table_data = []
            
            table_data.append(row_cells)
            continue
        else:
            # If we were in a table, it just ended. Create the table now.
            if in_table and table_data:
                # Calculate column widths dynamically based on content count
                col_count = len(table_data[0])
                avail_width = 460 # approx page width
                col_width = avail_width / col_count if col_count > 0 else 100
                
                t = Table(table_data, colWidths=[col_width] * col_count)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.teal), # Header Row Background
                    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke), # Header Text
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0,0), (-1,0), 8),
                    ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke), # Body Background
                    ('GRID', (0,0), (-1,-1), 0.5, colors.grey), # Borders
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('LEFTPADDING', (0,0), (-1,-1), 6),
                    ('RIGHTPADDING', (0,0), (-1,-1), 6),
                ]))
                flowables.append(t)
                flowables.append(Spacer(1, 12))
                
                in_table = False
                table_data = []

        # --- HEADER DETECTION ---
        if line.startswith('###'):
            header_text = line.replace('###', '').strip()
            h3 = ParagraphStyle('H3', parent=styles['Heading3'], textColor=colors.teal, spaceBefore=10, spaceAfter=6, fontSize=12)
            flowables.append(Paragraph(header_text, h3))
            continue
            
        # --- BOLD TEXT PARSING ---
        # Replace **text** with <b>text</b> for ReportLab
        formatted_line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
        
        # --- LIST DETECTION ---
        if line.startswith('* ') or line.startswith('- '):
            formatted_line = line[2:] # Remove marker
            flowables.append(Paragraph(f"• {formatted_line}", bullet_style))
        else:
            flowables.append(Paragraph(formatted_line, normal_style))
            
    # Catch table at end of text
    if in_table and table_data:
         col_count = len(table_data[0])
         avail_width = 460
         col_width = avail_width / col_count if col_count > 0 else 100
         t = Table(table_data, colWidths=[col_width] * col_count)
         t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.teal),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
             ('VALIGN', (0,0), (-1,-1), 'TOP'),
         ]))
         flowables.append(t)
         flowables.append(Spacer(1, 12))

    return flowables

# --- PDF ROUTE ---
@app.route('/download_summary/<session_id>')
@login_required
def download_summary(session_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT user_input, ai_response, timestamp, image_data FROM chat_logs 
            WHERE session_id = %s 
            ORDER BY timestamp ASC
        """, (session_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        if not rows:
            return render_template('no_conversation.html'), 404

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        styles = getSampleStyleSheet()
        story = []

        # Title
        title_style = ParagraphStyle('Title', parent=styles['Heading1'], alignment=1, spaceAfter=20, textColor=colors.teal)
        story.append(Paragraph("MediSimplify - Patient Report", title_style))
        story.append(Spacer(1, 12))

        # Disclaimer Box
        disclaimer_text = "<b>DISCLAIMER:</b> This report is generated by AI. It is <b>NOT</b> a medical diagnosis. Please consult a licensed doctor."
        d_style = ParagraphStyle('Disclaimer', parent=styles['Normal'], textColor=colors.darkred, backColor=colors.mistyrose, borderColor=colors.red, borderWidth=1, borderPadding=10, borderRadius=5, alignment=1)
        story.append(Paragraph(disclaimer_text, d_style))
        story.append(Spacer(1, 25))

        # Chat Styles
        style_user_label = ParagraphStyle('UserLabel', parent=styles['Normal'], textColor=colors.navy, fontName='Helvetica-Bold', spaceBefore=12)
        style_user_body = ParagraphStyle('UserBody', parent=styles['Normal'], textColor=colors.black, leftIndent=10, spaceAfter=10)
        
        style_ai_label = ParagraphStyle('AILabel', parent=styles['Normal'], textColor=colors.teal, fontName='Helvetica-Bold', spaceBefore=0)
        style_ai_container = ParagraphStyle('AIContainer', parent=styles['Normal'], spaceAfter=20, leftIndent=10)

        for row in rows:
            user_in, ai_out, ts, img_data = row
            time_str = ts.strftime("%Y-%m-%d %H:%M")
            
            # --- USER SECTION ---
            story.append(Paragraph(f"Patient ({time_str}):", style_user_label))
            story.append(Paragraph(user_in.replace("[Image Uploaded]", "<i>[Image Attachment]</i>"), style_user_body))
            
            # Image Attachment
            if img_data:
                try:
                    img_stream = io.BytesIO(img_data)
                    pdf_img = PDFImage(img_stream)
                    
                    # Smart Resize: Max width 4 inches
                    max_w = 300
                    aspect = pdf_img.drawHeight / pdf_img.drawWidth
                    pdf_img.drawWidth = max_w
                    pdf_img.drawHeight = max_w * aspect
                    
                    story.append(Spacer(1, 5))
                    story.append(pdf_img)
                    story.append(Spacer(1, 10))
                except Exception as e:
                    print(f"Image error: {e}")

            # --- AI SECTION ---
            story.append(Paragraph("MediSimplify Analysis:", style_ai_label))
            
            # Use the smart Markdown parser here!
            # We pass the raw AI text to our helper function
            ai_flowables = markdown_to_flowables(ai_out, styles)
            
            # Add all parsed elements (Tables, Headers, Text) to the story
            for flowable in ai_flowables:
                # Indent AI content slightly
                if hasattr(flowable, 'style'):
                    flowable.style.leftIndent = 10
                story.append(flowable)
                
            story.append(Spacer(1, 15))
            # Add a subtle divider line
            story.append(Paragraph("_" * 90, ParagraphStyle('Line', parent=styles['Normal'], textColor=colors.lightgrey, alignment=1)))

        doc.build(story)
        buffer.seek(0)

        return send_file(
            buffer,
            as_attachment=True,
            download_name=f'medical_summary_{session_id}.pdf',
            mimetype='application/pdf'
        )

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)