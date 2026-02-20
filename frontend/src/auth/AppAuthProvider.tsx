import { type ReactNode, useMemo } from "react";
import { Auth0Provider, useAuth0 } from "@auth0/auth0-react";

import { env } from "../config/env";
import { AuthContext, disabledAuthState } from "./AuthContext";
import type { AuthState } from "./types";

type Props = {
  children: ReactNode;
};

const AuthContextBridge = ({ children }: Props) => {
  const {
    isLoading,
    isAuthenticated,
    user,
    loginWithRedirect,
    logout,
    getAccessTokenSilently,
  } = useAuth0();

  const state = useMemo<AuthState>(
    () => ({
      enabled: true,
      isLoading,
      isAuthenticated,
      userEmail: user?.email ?? null,
      login: async () => {
        await loginWithRedirect();
      },
      logout: () => {
        logout({
          logoutParams: {
            returnTo: window.location.origin,
          },
        });
      },
      getAccessToken: async () => {
        try {
          return await getAccessTokenSilently({
            authorizationParams: {
              audience: env.auth0Audience,
            },
          });
        } catch {
          return null;
        }
      },
    }),
    [
      isLoading,
      isAuthenticated,
      user,
      loginWithRedirect,
      logout,
      getAccessTokenSilently,
    ],
  );

  return <AuthContext.Provider value={state}>{children}</AuthContext.Provider>;
};

export const AppAuthProvider = ({ children }: Props) => {
  if (!env.enableAuth || !env.auth0Domain || !env.auth0ClientId) {
    return (
      <AuthContext.Provider value={disabledAuthState}>
        {children}
      </AuthContext.Provider>
    );
  }

  return (
    <Auth0Provider
      domain={env.auth0Domain}
      clientId={env.auth0ClientId}
      authorizationParams={{
        redirect_uri: env.auth0RedirectUri,
        audience: env.auth0Audience,
      }}
      cacheLocation="localstorage"
      useRefreshTokens
    >
      <AuthContextBridge>{children}</AuthContextBridge>
    </Auth0Provider>
  );
};
