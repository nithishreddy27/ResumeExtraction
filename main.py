import fitz  # PyMuPDF
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import re
import os 
from fastapi.middleware.cors import CORSMiddleware

# Download necessary NLTK data files
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

app = FastAPI()


headings_list = [
    "Contact Information", "Name", "Address", "Phone Number", "Email", "LinkedIn Profile", "Personal Website",
    "Summary", "Objective", "Professional Summary", "Career Objective", "Profile",
    "Experience", "Professional Experience", "Work Experience", "Employment History", "Relevant Experience",
    "Education", "Academic Background", "Qualifications", "Degrees",
    "Skills", "Technical Skills", "Skills", "Core Competencies", "Key Skills",
    "Certifications", "Licenses", "Qualifications", "Training",
    "Projects", "Key Projects", "Personal Projects", "Research Projects",
    "Achievements", "Awards", "Honors", "Recognitions",
    "Languages", "Language Proficiency", "Multilingual Skills",
    "Professional Affiliations", "Professional Associations", "Memberships", "Affiliations",
    "Volunteer Experience", "Community Service", "Volunteering",
    "Publications", "Articles", "Research Papers",
    "Interests", "Hobbies",
    "References", "Recommendations", "Referees",
    "Additional Information", "Extra Details", "Miscellaneous"
]

desired_headings = [
    "Contact Information", "Summary", "Work Experience", "Education", "Skills", "Certifications", "Projects",
    "Achievements", "Languages", "Professional Affiliations", "Volunteer Experience", "Publications",
    "Interests", "References", "Additional Information"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to your client's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




def extract_text_with_positions(pdf_path):
    print("iNside positions")
    doc = fitz.open(pdf_path)
    text_positions = []
    for page in doc:
        for block in page.get_text("dict")["blocks"]:  # Use "dict" to get detailed information
            if block['type'] == 0:  # Text blocks
                for line in block['lines']:
                    for span in line['spans']:
                        text_positions.append({
                            'text': span['text'].strip(),
                            'bbox': span['bbox'],  # (x0, y0, x1, y1)
                            'font': span['font'],  # Font name
                            'size': span['size'],  # Font size
                            'color': span['color'],  # Font color in integer format
                            'flags': span['flags'],  # Font styles (e.g., bold, italic)
                        })
    doc.close()
    return text_positions

def extract_text_from_positions(text_positions):
    text = ""
    for i in text_positions:
        text+=i["text"]+" "
    return text








@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    pdf_path = f"./{file.filename}"
    print("new request came ",pdf_path)
    try:
        # Save the uploaded file
        with open(pdf_path, "wb") as f:
            f.write(await file.read())

        # Extract text positions and draw rectangles
        print("PDF Input Done")
        text_positions = extract_text_with_positions(pdf_path)
        print("Posititons done ",text_positions)
        aggregated_text = extract_text_from_positions(text_positions)
        print("aggregated text done ",aggregated_text)
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        print("Operations done returning")

        return JSONResponse(content={"text": aggregated_text , "TextPositions":text_positions})
        

    except Exception as e:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        return JSONResponse(content={"error": str(e)}, status_code=500)




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    