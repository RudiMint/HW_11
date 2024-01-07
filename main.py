import time

from fastapi import FastAPI, Depends, HTTPException, status, Path, Request, File, UploadFile
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from db import get_db
from models import Contact
from schemas import ContactResponse, ContactSchema

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/contacts", response_model=list[ContactResponse], tags=["contacts"])
async def get_contacts(db: Session = Depends(get_db)):
    contacts = db.query(Contact).all()
    return contacts


@app.get("/contact/{contact_id}", response_model=ContactResponse, tags=["contacts"])
async def get_contact_by_id(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@app.get("/contact/{contact_email}", response_model=ContactResponse, tags=["contacts"])
async def get_contact_by_email(contact_email: str = Path(ge=1), db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(email=contact_email).first()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@app.get("/contact/{first_name}", response_model=ContactResponse, tags=["contacts"])
async def get_contact_by_first_name(first_name: str = Path(ge=1), db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(first_name=first_name).first()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@app.get("/contact/{last_name}", response_model=ContactResponse, tags=["contacts"])
async def get_contact_by_last_name(last_name: str = Path(ge=1), db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(last_name=last_name).first()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@app.get("/contact/upcoming-birthdays", response_model=ContactResponse, tags=["contacts"])
async def get_upcoming_birthdays(db: Session = Depends(get_db)):
    today = datetime.now()
    upcoming_birthdays = db.query(Contact).filter_by(born_date=today + timedelta(days=7)).all()
    return upcoming_birthdays


@app.post("/add_contacts", response_model=ContactResponse, tags=["contacts"])
async def add_contact(contact: ContactSchema, db: Session = Depends(get_db)):
    contact_check = db.query(Contact).filter_by(email=contact.email).first()
    if contact_check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Contact already exists")
    new_contact = Contact(
        first_name=contact.first_name, last_name=contact.last_name, email=contact.email,
        phone=contact.phone, born_date=contact.born_date, description=contact.description
    )
    db.add(new_contact)
    db.commit()
    return new_contact



@app.put("/update_contacts/{contact_id}", response_model=ContactResponse, tags=["contacts"])
async def update_contact(contact: ContactSchema, contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    contact.first_name = ContactSchema.first_name
    contact.last_name = ContactSchema.last_name
    contact.email = ContactSchema.email
    contact.phone = ContactSchema.phone
    contact.born_date = ContactSchema.born_date
    contact.description = ContactSchema.description
    db.commit()
    return contact


@app.delete("/delete_contact/{contact_id}", response_model=ContactResponse, tags=["contacts"])
async def delete_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")

    db.delete(contact)
    db.commit()
    return contact



@app.get("/contacts")
def contacts(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="DB connection error")
        return {"contacts": [{"id": 1, "name": "John Doe"}]}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="DB connection error")


"""@app.post("/upload-file/")
async def create_upload_file(file: UploadFile = File()):
    pathlib.Path("uploads").mkdir(exist_ok=True)
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"file_path": file_path}"""
