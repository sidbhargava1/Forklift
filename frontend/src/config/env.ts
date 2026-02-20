const parseBoolean = (
  value: string | undefined,
  defaultValue: boolean,
): boolean => {
  if (value === undefined) {
    return defaultValue;
  }
  return value.toLowerCase() === "true";
};

export const env = {
  apiBaseUrl:
    import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1",
  enableAuth: parseBoolean(import.meta.env.VITE_ENABLE_AUTH, false),
  auth0Domain: import.meta.env.VITE_AUTH0_DOMAIN,
  auth0ClientId: import.meta.env.VITE_AUTH0_CLIENT_ID,
  auth0Audience: import.meta.env.VITE_AUTH0_AUDIENCE,
  auth0RedirectUri:
    import.meta.env.VITE_AUTH0_REDIRECT_URI ?? window.location.origin,
};
