import { Link, NavLink, Outlet, useParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useOrgs } from '../context/OrgContext';

export default function OrgLayout() {
  const { orgSlug } = useParams();
  const { organizations } = useOrgs();
  const { user, logout } = useAuth();

  const org = organizations.find((o) => o.slug === orgSlug);

  return (
    <div className="org-layout">
      <header className="topbar">
        <Link to="/orgs" className="brand">
          ← All orgs
        </Link>
        <h2>{org ? org.name : orgSlug}</h2>
        <nav>
          <NavLink to={`/orgs/${orgSlug}/projects`}>Projects</NavLink>
          <NavLink to={`/orgs/${orgSlug}/billing`}>Billing</NavLink>
        </nav>
        <div className="user-menu">
          <span>{user?.username}</span>
          <button onClick={logout}>Log out</button>
        </div>
      </header>
      <main>
        <Outlet />
      </main>
    </div>
  );
}
