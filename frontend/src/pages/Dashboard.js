import React, { useState, useEffect } from 'react';
import { studentService, attendanceService, gradeService, notificationService } from '../services/api';

function Dashboard({ user, onLogout }) {
  const [activeTab, setActiveTab] = useState('students');
  const [students, setStudents] = useState([]);
  const [attendance, setAttendance] = useState([]);
  const [grades, setGrades] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [s, a, g, n] = await Promise.all([
        studentService.getAll(),
        attendanceService.getAll(),
        gradeService.getAll(),
        notificationService.getAll(),
      ]);
      setStudents(s.data);
      setAttendance(a.data);
      setGrades(g.data);
      setNotifications(n.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'students', label: 'Students', count: students.length },
    { id: 'attendance', label: 'Attendance', count: attendance.length },
    { id: 'grades', label: 'Grades', count: grades.length },
    { id: 'notifications', label: 'Notifications', count: notifications.length },
  ];

  return (
    <div style={styles.container}>
      <nav style={styles.nav}>
        <div style={styles.navLeft}>
          <span style={styles.navLogo}>EduTrack</span>
          <span style={styles.navSchool}>{user?.school}</span>
        </div>
        <div style={styles.navRight}>
          <span style={styles.navUser}>{user?.first_name || user?.username}</span>
          <span style={styles.navRole}>{user?.role}</span>
          <button style={styles.logoutBtn} onClick={onLogout}>Logout</button>
        </div>
      </nav>

      <div style={styles.stats}>
        {tabs.map(tab => (
          <div key={tab.id} style={styles.statCard} onClick={() => setActiveTab(tab.id)}>
            <div style={styles.statNum}>{tab.count}</div>
            <div style={styles.statLabel}>{tab.label}</div>
          </div>
        ))}
      </div>

      <div style={styles.tabs}>
        {tabs.map(tab => (
          <button
            key={tab.id}
            style={{ ...styles.tab, ...(activeTab === tab.id ? styles.activeTab : {}) }}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div style={styles.content}>
        {loading ? (
          <div style={styles.loading}>Loading...</div>
        ) : (
          <>
            {activeTab === 'students' && <StudentsTable students={students} onRefresh={loadData} />}
            {activeTab === 'attendance' && <AttendanceTable attendance={attendance} onRefresh={loadData} />}
            {activeTab === 'grades' && <GradesTable grades={grades} onRefresh={loadData} />}
            {activeTab === 'notifications' && <NotificationsTable notifications={notifications} />}
          </>
        )}
      </div>
    </div>
  );
}

function StudentsTable({ students, onRefresh }) {
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({
    first_name: '', last_name: '', student_id: '',
    date_of_birth: '', gender: 'Male', class_name: '',
    school: '', parent_phone: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await studentService.create(form);
      setShowForm(false);
      setForm({ first_name: '', last_name: '', student_id: '', date_of_birth: '', gender: 'Male', class_name: '', school: '', parent_phone: '' });
      onRefresh();
    } catch (err) {
      alert('Error creating student');
    }
  };

  return (
    <div>
      <div style={styles.tableHeader}>
        <h2 style={styles.tableTitle}>Students</h2>
        <button style={styles.addBtn} onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ Add Student'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} style={styles.form}>
          <div style={styles.formGrid}>
            {[
              ['first_name', 'First Name', 'text'],
              ['last_name', 'Last Name', 'text'],
              ['student_id', 'Student ID', 'text'],
              ['date_of_birth', 'Date of Birth', 'date'],
              ['class_name', 'Class', 'text'],
              ['school', 'School', 'text'],
              ['parent_phone', 'Parent Phone', 'text'],
            ].map(([key, label, type]) => (
              <div key={key}>
                <label style={styles.label}>{label}</label>
                <input
                  style={styles.input}
                  type={type}
                  value={form[key]}
                  onChange={(e) => setForm({ ...form, [key]: e.target.value })}
                  required
                />
              </div>
            ))}
            <div>
              <label style={styles.label}>Gender</label>
              <select style={styles.input} value={form.gender} onChange={(e) => setForm({ ...form, gender: e.target.value })}>
                <option>Male</option>
                <option>Female</option>
              </select>
            </div>
          </div>
          <button type="submit" style={styles.addBtn}>Save Student</button>
        </form>
      )}

      <table style={styles.table}>
        <thead>
          <tr>
            {['Student ID', 'Name', 'Class', 'School', 'Gender', 'Parent Phone', 'Status'].map(h => (
              <th key={h} style={styles.th}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {students.map(s => (
            <tr key={s.id} style={styles.tr}>
              <td style={styles.td}>{s.student_id}</td>
              <td style={styles.td}>{s.first_name} {s.last_name}</td>
              <td style={styles.td}>{s.class_name}</td>
              <td style={styles.td}>{s.school}</td>
              <td style={styles.td}>{s.gender}</td>
              <td style={styles.td}>{s.parent_phone}</td>
              <td style={styles.td}>
                <span style={{ ...styles.badge, background: s.is_active ? '#dcfce7' : '#fee2e2', color: s.is_active ? '#166534' : '#991b1b' }}>
                  {s.is_active ? 'Active' : 'Inactive'}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function AttendanceTable({ attendance, onRefresh }) {
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({
    student_id: '', student_name: '', class_name: '',
    school: '', date: '', status: 'present', recorded_by: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await attendanceService.create(form);
      setShowForm(false);
      onRefresh();
    } catch (err) {
      alert('Error recording attendance');
    }
  };

  const statusColors = {
    present: { bg: '#dcfce7', color: '#166534' },
    absent: { bg: '#fee2e2', color: '#991b1b' },
    late: { bg: '#fef9c3', color: '#854d0e' },
    excused: { bg: '#dbeafe', color: '#1e40af' },
  };

  return (
    <div>
      <div style={styles.tableHeader}>
        <h2 style={styles.tableTitle}>Attendance</h2>
        <button style={styles.addBtn} onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ Record Attendance'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} style={styles.form}>
          <div style={styles.formGrid}>
            {[
              ['student_id', 'Student ID', 'text'],
              ['student_name', 'Student Name', 'text'],
              ['class_name', 'Class', 'text'],
              ['school', 'School', 'text'],
              ['date', 'Date', 'date'],
              ['recorded_by', 'Recorded By', 'text'],
            ].map(([key, label, type]) => (
              <div key={key}>
                <label style={styles.label}>{label}</label>
                <input style={styles.input} type={type} value={form[key]} onChange={(e) => setForm({ ...form, [key]: e.target.value })} required />
              </div>
            ))}
            <div>
              <label style={styles.label}>Status</label>
              <select style={styles.input} value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>
                <option value="present">Present</option>
                <option value="absent">Absent</option>
                <option value="late">Late</option>
                <option value="excused">Excused</option>
              </select>
            </div>
          </div>
          <button type="submit" style={styles.addBtn}>Save</button>
        </form>
      )}

      <table style={styles.table}>
        <thead>
          <tr>
            {['Student ID', 'Name', 'Class', 'Date', 'Status', 'Recorded By'].map(h => (
              <th key={h} style={styles.th}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {attendance.map(a => (
            <tr key={a.id} style={styles.tr}>
              <td style={styles.td}>{a.student_id}</td>
              <td style={styles.td}>{a.student_name}</td>
              <td style={styles.td}>{a.class_name}</td>
              <td style={styles.td}>{a.date}</td>
              <td style={styles.td}>
                <span style={{ ...styles.badge, background: statusColors[a.status]?.bg, color: statusColors[a.status]?.color }}>
                  {a.status}
                </span>
              </td>
              <td style={styles.td}>{a.recorded_by}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function GradesTable({ grades, onRefresh }) {
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({
    student_id: '', student_name: '', class_name: '', school: '',
    subject: '', score: '', max_score: 100, term: 'Term 1', year: 2026, recorded_by: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await gradeService.create(form);
      setShowForm(false);
      onRefresh();
    } catch (err) {
      alert('Error recording grade');
    }
  };

  return (
    <div>
      <div style={styles.tableHeader}>
        <h2 style={styles.tableTitle}>Grades</h2>
        <button style={styles.addBtn} onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ Record Grade'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} style={styles.form}>
          <div style={styles.formGrid}>
            {[
              ['student_id', 'Student ID', 'text'],
              ['student_name', 'Student Name', 'text'],
              ['class_name', 'Class', 'text'],
              ['school', 'School', 'text'],
              ['subject', 'Subject', 'text'],
              ['score', 'Score', 'number'],
              ['max_score', 'Max Score', 'number'],
              ['year', 'Year', 'number'],
              ['recorded_by', 'Recorded By', 'text'],
            ].map(([key, label, type]) => (
              <div key={key}>
                <label style={styles.label}>{label}</label>
                <input style={styles.input} type={type} value={form[key]} onChange={(e) => setForm({ ...form, [key]: e.target.value })} required />
              </div>
            ))}
            <div>
              <label style={styles.label}>Term</label>
              <select style={styles.input} value={form.term} onChange={(e) => setForm({ ...form, term: e.target.value })}>
                <option>Term 1</option>
                <option>Term 2</option>
                <option>Term 3</option>
              </select>
            </div>
          </div>
          <button type="submit" style={styles.addBtn}>Save</button>
        </form>
      )}

      <table style={styles.table}>
        <thead>
          <tr>
            {['Student ID', 'Name', 'Subject', 'Score', 'Grade', 'Term', 'Year'].map(h => (
              <th key={h} style={styles.th}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {grades.map(g => (
            <tr key={g.id} style={styles.tr}>
              <td style={styles.td}>{g.student_id}</td>
              <td style={styles.td}>{g.student_name}</td>
              <td style={styles.td}>{g.subject}</td>
              <td style={styles.td}>{g.score}/{g.max_score} ({g.percentage}%)</td>
              <td style={styles.td}>
                <span style={{ ...styles.badge, background: '#dbeafe', color: '#1e40af' }}>{g.grade_letter}</span>
              </td>
              <td style={styles.td}>{g.term}</td>
              <td style={styles.td}>{g.year}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function NotificationsTable({ notifications }) {
  const statusColors = {
    sent: { bg: '#dcfce7', color: '#166534' },
    pending: { bg: '#fef9c3', color: '#854d0e' },
    failed: { bg: '#fee2e2', color: '#991b1b' },
  };

  return (
    <div>
      <div style={styles.tableHeader}>
        <h2 style={styles.tableTitle}>Notifications</h2>
      </div>
      <table style={styles.table}>
        <thead>
          <tr>
            {['Recipient', 'Type', 'Subject', 'Status', 'Sent At'].map(h => (
              <th key={h} style={styles.th}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {notifications.map(n => (
            <tr key={n.id} style={styles.tr}>
              <td style={styles.td}>{n.recipient_name}</td>
              <td style={styles.td}>{n.notification_type}</td>
              <td style={styles.td}>{n.subject}</td>
              <td style={styles.td}>
                <span style={{ ...styles.badge, background: statusColors[n.status]?.bg, color: statusColors[n.status]?.color }}>
                  {n.status}
                </span>
              </td>
              <td style={styles.td}>{n.sent_at ? new Date(n.sent_at).toLocaleString() : '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const styles = {
  container: { minHeight: '100vh', background: '#f0f4f8', fontFamily: 'sans-serif' },
  nav: { background: '#fff', padding: '0 32px', height: 60, display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid #e5e7eb' },
  navLeft: { display: 'flex', alignItems: 'center', gap: 16 },
  navLogo: { fontSize: 22, fontWeight: 700, color: '#2563eb' },
  navSchool: { fontSize: 13, color: '#6b7280' },
  navRight: { display: 'flex', alignItems: 'center', gap: 12 },
  navUser: { fontSize: 14, fontWeight: 500, color: '#111827' },
  navRole: { fontSize: 12, background: '#dbeafe', color: '#1e40af', padding: '2px 8px', borderRadius: 20 },
  logoutBtn: { background: 'none', border: '1px solid #d1d5db', borderRadius: 6, padding: '6px 14px', cursor: 'pointer', fontSize: 13, color: '#374151' },
  stats: { display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, padding: '24px 32px 0' },
  statCard: { background: '#fff', borderRadius: 10, padding: '20px 24px', cursor: 'pointer', border: '1px solid #e5e7eb' },
  statNum: { fontSize: 32, fontWeight: 700, color: '#2563eb' },
  statLabel: { fontSize: 13, color: '#6b7280', marginTop: 4 },
  tabs: { display: 'flex', gap: 4, padding: '20px 32px 0' },
  tab: { padding: '8px 20px', border: 'none', background: 'none', cursor: 'pointer', fontSize: 14, color: '#6b7280', borderRadius: 6 },
  activeTab: { background: '#2563eb', color: '#fff' },
  content: { margin: '16px 32px', background: '#fff', borderRadius: 10, padding: 24, border: '1px solid #e5e7eb' },
  loading: { textAlign: 'center', padding: 40, color: '#6b7280' },
  tableHeader: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 },
  tableTitle: { fontSize: 18, fontWeight: 600, color: '#111827', margin: 0 },
  addBtn: { background: '#2563eb', color: '#fff', border: 'none', borderRadius: 6, padding: '8px 16px', cursor: 'pointer', fontSize: 13, fontWeight: 500 },
  form: { background: '#f9fafb', borderRadius: 8, padding: 20, marginBottom: 20, border: '1px solid #e5e7eb' },
  formGrid: { display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 16 },
  table: { width: '100%', borderCollapse: 'collapse' },
  th: { textAlign: 'left', padding: '10px 14px', fontSize: 12, fontWeight: 600, color: '#6b7280', borderBottom: '1px solid #e5e7eb', textTransform: 'uppercase' },
  tr: { borderBottom: '1px solid #f3f4f6' },
  td: { padding: '12px 14px', fontSize: 14, color: '#374151' },
  badge: { padding: '2px 10px', borderRadius: 20, fontSize: 12, fontWeight: 500 },
  label: { display: 'block', fontSize: 12, fontWeight: 500, color: '#374151', marginBottom: 4 },
  input: { width: '100%', padding: '8px 12px', border: '1px solid #d1d5db', borderRadius: 6, fontSize: 13, boxSizing: 'border-box' },
};

export default Dashboard;
