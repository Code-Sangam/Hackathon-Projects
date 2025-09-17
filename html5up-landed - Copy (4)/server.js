require('dotenv').config();
const path = require('path');
const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
const sqlite3 = require('sqlite3').verbose();

const app = express();
const PORT = process.env.PORT || 3000;

// Middlewares
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Static frontend
app.use(express.static(path.join(__dirname)));

// MongoDB setup
const mongoUri = process.env.MONGO_URI || 'mongodb://127.0.0.1:27017/alumni_platform';
mongoose.set('strictQuery', false);
mongoose.connect(mongoUri).then(() => console.log('MongoDB connected')).catch(err => console.error('MongoDB error:', err.message));

const userSchema = new mongoose.Schema({
  userType: { type: String, enum: ['student', 'alumni'], required: true },
  fullName: String,
  rollNo: String,
  collegeName: String,
  department: String, // student only
  currentRole: String, // alumni only
  address: String,
  email: String,
  mobile: String,
  password: String, // simple placeholder
  createdAt: { type: Date, default: Date.now }
});
const User = mongoose.model('User', userSchema);

// SQLite setup
const db = new sqlite3.Database(path.join(__dirname, 'auth.sqlite'));
db.serialize(() => {
  db.run(`CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userType TEXT NOT NULL,
    fullName TEXT,
    rollNo TEXT,
    collegeName TEXT,
    department TEXT,
    currentRole TEXT,
    address TEXT,
    email TEXT,
    mobile TEXT,
    password TEXT,
    createdAt TEXT
  )`);
});

function insertSqlite(user){
  db.run(
    `INSERT INTO users (userType, fullName, rollNo, collegeName, department, currentRole, address, email, mobile, password, createdAt)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
    [user.userType, user.fullName, user.rollNo, user.collegeName, user.department || null, user.currentRole || null, user.address, user.email || null, user.mobile || null, user.password || null, new Date().toISOString()],
    err => { if (err) console.error('SQLite insert error:', err.message); }
  );
}

// Helpers
function requireContact(req, res){
  if(!req.body.email && !req.body.mobile){
    res.status(400).json({ success:false, message: 'Provide email or mobile' });
    return false;
  }
  return true;
}

// Routes
app.post('/api/signup/student', async (req, res) => {
  try {
    if(!requireContact(req, res)) return;
    const { fullName, rollNo, collegeName, department, address, email, mobile } = req.body;
    const doc = await User.create({ userType: 'student', fullName, rollNo, collegeName, department, address, email, mobile });
    insertSqlite(doc.toObject());
    res.json({ success:true, message:'Student signup stored' });
  } catch (e) {
    console.error(e);
    res.status(500).json({ success:false, message:'Server error' });
  }
});

app.post('/api/signup/alumni', async (req, res) => {
  try {
    if(!requireContact(req, res)) return;
    const { fullName, rollNo, collegeName, currentRole, address, email, mobile } = req.body;
    const doc = await User.create({ userType: 'alumni', fullName, rollNo, collegeName, currentRole, address, email, mobile });
    insertSqlite(doc.toObject());
    res.json({ success:true, message:'Alumni signup stored' });
  } catch (e) {
    console.error(e);
    res.status(500).json({ success:false, message:'Server error' });
  }
});

app.post('/api/login', async (req, res) => {
  try {
    const { email, mobile, password } = req.body;
    if(!email && !mobile) return res.status(400).json({ success:false, message:'Provide email or mobile' });
    const user = await User.findOne({ $or: [ { email }, { mobile } ] }).lean();
    if(!user) return res.status(401).json({ success:false, message:'User not found' });
    // Password is optional in this demo; accept login if user exists
    res.json({ success:true, message:'Login success' });
  } catch (e) {
    console.error(e);
    res.status(500).json({ success:false, message:'Server error' });
  }
});

app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
