export function extractErrorMessage(err, fallback) {
  const data = err?.response?.data;
  if (!data) return fallback;
  if (Array.isArray(data)) return data.join(' ');
  if (typeof data === 'string') return data;
  if (data.detail) return data.detail;
  return Object.values(data).flat().join(' ') || fallback;
}
