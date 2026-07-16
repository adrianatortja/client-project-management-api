import { useEffect, useState } from 'react';
import { useParams, useSearchParams } from 'react-router-dom';
import client from '../api/client';
import { extractErrorMessage } from '../api/errors';

export default function BillingPage() {
  const { orgSlug } = useParams();
  const [searchParams] = useSearchParams();
  const [subscription, setSubscription] = useState(null);
  const [error, setError] = useState('');
  const [redirecting, setRedirecting] = useState(false);

  async function load() {
    const { data } = await client.get(`/api/orgs/${orgSlug}/billing/`);
    setSubscription(data);
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [orgSlug]);

  async function handleUpgrade() {
    setError('');
    setRedirecting(true);
    try {
      const { data } = await client.post(`/api/orgs/${orgSlug}/billing/checkout/`);
      window.location.href = data.checkout_url;
    } catch (err) {
      setError(extractErrorMessage(err, 'Could not start checkout.'));
      setRedirecting(false);
    }
  }

  async function handleManage() {
    setError('');
    setRedirecting(true);
    try {
      const { data } = await client.post(`/api/orgs/${orgSlug}/billing/portal/`);
      window.location.href = data.portal_url;
    } catch (err) {
      setError(extractErrorMessage(err, 'Could not open billing portal.'));
      setRedirecting(false);
    }
  }

  if (!subscription) return <p>Loading billing info…</p>;

  const checkoutResult = searchParams.get('checkout');

  return (
    <div className="page">
      <h1>Billing</h1>

      {checkoutResult === 'success' && <p className="success">Checkout complete — thanks!</p>}
      {checkoutResult === 'cancel' && <p className="muted">Checkout canceled.</p>}

      <div className="plan-card">
        <p>
          Current plan: <strong>{subscription.plan}</strong>
        </p>
        <p className="muted">
          {subscription.max_projects === null
            ? 'Unlimited projects'
            : `Up to ${subscription.max_projects} projects`}
        </p>
        <p className="muted">Status: {subscription.status}</p>

        {subscription.plan === 'free' ? (
          <button onClick={handleUpgrade} disabled={redirecting}>
            {redirecting ? 'Redirecting…' : 'Upgrade to Pro'}
          </button>
        ) : (
          <button onClick={handleManage} disabled={redirecting}>
            {redirecting ? 'Redirecting…' : 'Manage billing'}
          </button>
        )}
      </div>
      {error && <p className="error">{error}</p>}
    </div>
  );
}
