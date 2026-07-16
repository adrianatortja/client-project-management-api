import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import client from '../api/client';

export default function ProjectDetailPage() {
  const { orgSlug, projectId } = useParams();
  const [project, setProject] = useState(null);
  const [taskTitle, setTaskTitle] = useState('');
  const [error, setError] = useState('');

  async function load() {
    const { data } = await client.get(`/api/orgs/${orgSlug}/projects/${projectId}/`);
    setProject(data);
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [orgSlug, projectId]);

  async function handleAddTask(e) {
    e.preventDefault();
    setError('');
    try {
      await client.post(`/api/orgs/${orgSlug}/projects/tasks/`, {
        project: Number(projectId),
        title: taskTitle,
      });
      setTaskTitle('');
      await load();
    } catch (err) {
      setError('Could not add task.');
    }
  }

  async function toggleTask(task) {
    await client.patch(`/api/orgs/${orgSlug}/projects/tasks/${task.id}/`, {
      completed: !task.completed,
    });
    await load();
  }

  async function deleteTask(task) {
    await client.delete(`/api/orgs/${orgSlug}/projects/tasks/${task.id}/`);
    await load();
  }

  if (!project) return <p>Loading project…</p>;

  return (
    <div className="page">
      <Link to={`/orgs/${orgSlug}/projects`}>← Back to projects</Link>
      <h1>{project.title}</h1>
      <p className="muted">{project.description}</p>
      <p>
        <span className="badge">{project.status}</span> · {project.completed_tasks}/
        {project.total_tasks} tasks complete
      </p>

      <h2>Tasks</h2>
      <ul className="task-list">
        {project.tasks.map((task) => (
          <li key={task.id} className={task.completed ? 'completed' : ''}>
            <label>
              <input
                type="checkbox"
                checked={task.completed}
                onChange={() => toggleTask(task)}
              />
              {task.title}
            </label>
            <button className="link-button" onClick={() => deleteTask(task)}>
              Delete
            </button>
          </li>
        ))}
        {project.tasks.length === 0 && <p className="muted">No tasks yet.</p>}
      </ul>

      <form className="inline-form" onSubmit={handleAddTask}>
        <input
          placeholder="New task title"
          value={taskTitle}
          onChange={(e) => setTaskTitle(e.target.value)}
          required
        />
        <button type="submit">Add task</button>
      </form>
      {error && <p className="error">{error}</p>}
    </div>
  );
}
