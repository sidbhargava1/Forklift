import { useState } from "react";

import { fetchHealth, fetchIntegrationStatus, fetchMe } from "./api/client";
import { useAuth } from "./hooks/useAuth";

export const App = () => {
  const auth = useAuth();
  const [healthResult, setHealthResult] = useState<string>("");
  const [integrationsResult, setIntegrationsResult] = useState<string>("");
  const [claimsResult, setClaimsResult] = useState<string>("");
  const [error, setError] = useState<string>("");

  const onLoadHealth = async () => {
    setError("");
    try {
      const payload = await fetchHealth();
      setHealthResult(JSON.stringify(payload, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unexpected error");
    }
  };

  const onLoadIntegrations = async () => {
    setError("");
    try {
      const payload = await fetchIntegrationStatus();
      setIntegrationsResult(JSON.stringify(payload, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unexpected error");
    }
  };

  const onLoadClaims = async () => {
    setError("");
    try {
      const token = auth.enabled ? await auth.getAccessToken() : null;
      const payload = await fetchMe(token);
      setClaimsResult(JSON.stringify(payload, null, 2));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unexpected error");
    }
  };

  return (
    <main className="page">
      <section className="hero">
        <p className="eyebrow">FastAPI + React + Postgres + Redis + Auth0 + OpenAI</p>
        <h1>Codex App Starter</h1>
        <p className="subtitle">
          This template provides infrastructure and reusable connectors only. Product-specific APIs
          and UI are intentionally left for your app layer.
        </p>
      </section>

      <section className="panel">
        <h2>Backend checks</h2>
        <div className="panel-row actions">
          <button type="button" onClick={onLoadHealth}>
            GET /health
          </button>
          <button type="button" onClick={onLoadIntegrations}>
            GET /health/integrations
          </button>
        </div>
        {healthResult ? <pre className="code-block">{healthResult}</pre> : null}
        {integrationsResult ? <pre className="code-block">{integrationsResult}</pre> : null}
      </section>

      <section className="panel">
        <h2>Auth0 wiring</h2>
        <p>
          {auth.enabled
            ? auth.isAuthenticated
              ? `Signed in as ${auth.userEmail ?? "unknown user"}`
              : "Auth enabled, not signed in"
            : "Auth disabled (set VITE_ENABLE_AUTH=true and Auth0 env vars)."}
        </p>

        <div className="panel-row actions">
          <button
            type="button"
            onClick={auth.login}
            disabled={!auth.enabled || auth.isAuthenticated}
          >
            Log in
          </button>
          <button
            type="button"
            onClick={auth.logout}
            disabled={!auth.enabled || !auth.isAuthenticated}
          >
            Log out
          </button>
          <button type="button" onClick={onLoadClaims}>
            GET /auth/me
          </button>
        </div>

        {claimsResult ? <pre className="code-block">{claimsResult}</pre> : null}
      </section>

      {error ? <p className="error">{error}</p> : null}
    </main>
  );
};
