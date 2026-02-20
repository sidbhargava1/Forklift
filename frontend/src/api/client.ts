import { env } from "../config/env";

const buildHeaders = (token: string | null) => {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  return headers;
};

export const fetchHealth = async () => {
  const response = await fetch(`${env.apiBaseUrl}/health`);
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Failed to fetch backend health.");
  }
  return response.json();
};

export const fetchIntegrationStatus = async () => {
  const response = await fetch(`${env.apiBaseUrl}/health/integrations`);
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Failed to fetch integration status.");
  }
  return response.json();
};

export const fetchMe = async (token: string | null) => {
  const response = await fetch(`${env.apiBaseUrl}/auth/me`, {
    method: "GET",
    headers: buildHeaders(token),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Failed to fetch /auth/me.");
  }

  return response.json();
};
