import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import client from '../api/client';
import { extractErrorMessage } from '../api/errors';

export default function ProjectListPage() {
  const { orgSlug } = useParams();
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [status, setStatus] = useState('');
  const [search, setSearch] = useState('');
  const [ordering, setOrdering] = useState('-created_at');
  const [title, setTitle] = useState('');
  const [creating, setCreating] = useState(false);

  async function load() {
    setLoading(true);
    const params = { ordering };
    if (status) params.status = status;
    if (search) params.search = search;
    const { data } = await client.get(`/api/orgs/${orgSlug}/projects/`, { params });
    setProjects(data);
    setLoading(false);
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [orgSlug, status, search, ordering]);

  async function handleCreate(e) {
    e.preventDefault();
    setError('');
    setCreating(true);
    try {
      await client.post(`/api/orgs/${orgSlug}/projects/`, { title, status: 'active' });
      setTitle('');
      await load();
    } catch (err) {
      setError(extractErrorMessage(err, 'Could not create project.'));
    } finally {
      setCreating(false);
    }
  }

  return (
    <div className="page">
      <h1>Projects</h1>

      <div className="filters">
        <input
          placeholder="Search by title…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="">All statuses</option>
          <option value="active">Active</option>
          <option value="completed">Completed</option>
        </select>
        <select value={ordering} onChange={(e) => setOrdering(e.target.value)}>
          <option value="-created_at">Newest first</option>
          <option value="created_at">Oldest first</option>
          <option value="title">Title A–Z</option>
          <option value="-title">Title Z–A</option>
        </select>
      </div>

      {loading ? (
        <p>Loading projects…</p>
      ) : (
        <ul className="project-list">
          {projects.map((project) => (
            <li key={project.id}>
              <Link to={`/orgs/${orgSlug}/projects/${project.id}`}>{project.title}</Link>
              <span className="badge">{project.status}</span>
              <span className="muted">
                {' '}
                {project.completed_tasks}/{project.total_tasks} tasks done
              </span>
            </li>
          ))}
          {projects.length === 0 && <p className="muted">No projects yet.</p>}
        </ul>
      )}

      <form className="inline-form" onSubmit={handleCreate}>
        <input
          placeholder="New project title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <button type="submit" disabled={creating}>
          {creating ? 'Creating…' : 'Create project'}
        </button>
      </form>
      {error && <p className="error">{error}</p>}
    </div>
  );
}
