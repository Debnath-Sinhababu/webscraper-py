from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
from models import Base, Item, DashboardData, CompanyData, TransportData

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Set up SQLite database connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Dependency to provide a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Create a new item
@app.post("/items/")
def create_item(name: str, db: Session = Depends(get_db)):
    item = Item(name=name)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# Get all items as an HTML table
@app.get("/items/", response_class=HTMLResponse)
def read_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()

    # Build an HTML table
    table = """
    <html>
        <head>
            <title>Items List</title>
        </head>
        <body>
            <h1>Items</h1>
            <table border="1">
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                </tr>
    """

    # Add each item as a table row
    for item in items:
        table += f"""
                <tr>
                    <td>{item.id}</td>
                    <td>{item.name}</td>
                </tr>
        """

    table += """
            </table>
        </body>
    </html>
    """

    return table

# Get all items as an HTML table
@app.get("/dashboard/all", response_class=JSONResponse)
def read_items(db: Session = Depends(get_db)):
    items = db.query(DashboardData).all()
    return items

@app.get("/dashboard/transport", response_class=JSONResponse)
def read_items(db: Session = Depends(get_db)):
    items = db.query(TransportData).all()
    return items

@app.get("/dashboard/company", response_class=JSONResponse)
def read_items(db: Session = Depends(get_db)):
    items = db.query(CompanyData).all()
    return items

# Optional: Set a default route to serve the HTML file
@app.get("/")
async def read_index():
    return {"message": "Go to /static/index.html to see the HTML file"}