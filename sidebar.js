// sidebar.js — inject sidebar + topbar into teacher pages
// Usage: <script src="sidebar.js"></script> then call initPage(pageId, pageTitle, pageSub)

function buildSidebar(activeId) {
  const teacher = localStorage.getItem('teacherName') || 'Teacher';
  const initials = teacher.split(' ').map(w => w[0]).join('').toUpperCase().slice(0,2);

  const navItems = [
    { id: 'dashboard',  icon: '⊞', label: 'Dashboard',        href: 'teacher-dashboard.html' },
    { id: 'questions',  icon: '❓', label: 'Questions',         href: 'teacher-questions.html' },
    { id: 'create',     icon: '✏️', label: 'Create Question',   href: 'teacher-create-question.html' },
    { id: 'generate',   icon: '✨', label: 'Generate Question', href: 'teacher-generate-question.html' },
    { id: 'students',   icon: '👥', label: 'Students',          href: 'teacher-students.html' },
    { id: 'analytics', icon: '📊', label: 'Class Analytics', href: 'class-analytics.html' },
  ];

  const navHTML = navItems.map(item => `
    <a href="${item.href}" class="nav-item${item.id === activeId ? ' active' : ''}">
      <span class="nav-icon">${item.icon}</span>
      ${item.label}
    </a>
  `).join('');

  return `
    <nav class="sidebar">
      <a class="sidebar-logo" href="teacher-dashboard.html">
        <div class="sidebar-logo-img">
          <img src="images/logo.png" alt="TeacherAId"/>
        </div>
        <div class="sidebar-logo-text">Teacher<span>AId</span></div>
      </a>
      <div class="sidebar-section">Navigation</div>
      ${navHTML}
      <div class="sidebar-spacer"></div>
      <div class="sidebar-footer">
        <div class="teacher-badge">
          <div class="teacher-avatar">${initials}</div>
          <div class="teacher-info">
            <div class="t-name">${teacher}</div>
            <div class="t-role">Teacher</div>
          </div>
        </div>
        <a href="index.html" class="nav-item" style="margin-top:8px; color:rgba(255,255,255,.4);">
          <span class="nav-icon">←</span> Sign out
        </a>
      </div>
    </nav>
  `;
}

function initPage(pageId, title, sub) {
  document.body.innerHTML = buildSidebar(pageId) +
    `<div class="main" id="mainContent">
      <div class="topbar">
        <div>
          <div class="topbar-title">${title}</div>
          ${sub ? `<div class="topbar-sub">${sub}</div>` : ''}
        </div>
      </div>
      <div class="page-content" id="pageContent"></div>
    </div>`;
}
