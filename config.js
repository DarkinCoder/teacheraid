// ── TeacherAId Backend Config ──────────────────────────────
// All API calls go through the FastAPI backend only.
// Never put DeepSeek or Moorcheh keys here.

const API_BASE = "https://unhoofed-noble-rowdyishly.ngrok-free.dev";

// Derive stable IDs from stored names
function getTeacherId()   { return localStorage.getItem('teacherName')  || 'teacher_001'; }
function getClassroomId() {
  const t = localStorage.getItem('teacherName') || 'classroom';
  return 'cls_' + t.toLowerCase().replace(/\s+/g, '_');
}
function getStudentId()   { return localStorage.getItem('currentStudent') || 'student_001'; }

// Active question_id set after teacher creates a question
function getActiveQuestionId() { return localStorage.getItem('activeQuestionId') || null; }
function setActiveQuestionId(id) { localStorage.setItem('activeQuestionId', id); }

// ── Generic fetch helpers ──────────────────────────────────
async function apiGet(path) {
  const res = await fetch(API_BASE + path, {
    headers: { 'ngrok-skip-browser-warning': 'true' }
  });
  if (res.status === 404) return null;  // no data yet, not an error
  if (!res.ok) throw new Error(`GET ${path} → ${res.status}`);
  return res.json();
}

async function apiPost(path, body) {
  const res = await fetch(API_BASE + path, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'ngrok-skip-browser-warning': 'true'
    },
    body: JSON.stringify(body)
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`POST ${path} → ${res.status}: ${err}`);
  }
  return res.json();
}
