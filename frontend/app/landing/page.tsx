'use client';

import { useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { GoogleIcon } from '@/components/ui/google-icon'; // Assuming you have this component or will create it

export default function LandingPage() {
  useEffect(() => {
    // Check if a token already exists in local storage
    const token = localStorage.getItem('access_token');
    if (token) {
      // If token exists, redirect to the main app page
      window.location.href = '/';
    }
  }, []);

  const handleGoogleSignIn = () => {
    // Redirect to your backend's Google OAuth initiation endpoint
    window.location.href = 'http://localhost:8000/auth/google';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-md shadow-lg text-center">
        <CardHeader>
          <CardTitle className="text-3xl font-bold">Welcome to the LLM-Powered Query System</CardTitle>
          <CardDescription className="mt-2">Your intelligent assistant for document retrieval.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <p className="text-lg text-gray-700">
            Sign in to access your documents and start querying.
          </p>
          <Button 
            onClick={handleGoogleSignIn}
            className="w-full py-3 text-lg bg-blue-600 hover:bg-blue-700 text-white flex items-center justify-center space-x-2"
          >
            <GoogleIcon className="w-6 h-6" />
            <span>Sign in with Google</span>
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
