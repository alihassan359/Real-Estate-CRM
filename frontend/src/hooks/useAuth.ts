/**
 * useAuth Hook - Custom Hook for Authentication
 */


import { useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuthStore } from '@/store/authStore';
import { AuthService, LoginRequest, SignupRequest } from '@/services/auth.service';

export function useAuth() {
  const queryClient = useQueryClient();
  const { user, token, logout: logoutStore, setUser, setToken } = useAuthStore();

  // Login mutation
  const loginMutation = useMutation({
    mutationFn: (credentials: LoginRequest) => AuthService.login(credentials),
    onSuccess: (data) => {
      // data.data contains { accessToken, refreshToken, user }
      const { accessToken, user: userData } = data.data;
      setToken(accessToken);
      setUser(userData as any);
      queryClient.invalidateQueries({ queryKey: ['auth'] });
    },
  });

  // Signup mutation
  const signupMutation = useMutation({
    mutationFn: (data: SignupRequest) => AuthService.signup(data),
    onSuccess: (data) => {
      const { accessToken, user: userData } = data.data;
      setToken(accessToken);
      setUser(userData as any);
      queryClient.invalidateQueries({ queryKey: ['auth'] });
    },
  });

  // Logout
  const logout = useCallback(async () => {
    try {
      await AuthService.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      logoutStore();
      queryClient.clear();
    }
  }, [logoutStore, queryClient]);

  return {
    user,
    token,
    isAuthenticated: !!token,
    login: loginMutation.mutate,
    loginAsync: loginMutation.mutateAsync,
    isLoggingIn: loginMutation.isPending,
    signup: signupMutation.mutate,
    signupAsync: signupMutation.mutateAsync,
    isSigningUp: signupMutation.isPending,
    logout,
  };
}

