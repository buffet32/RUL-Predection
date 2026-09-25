import React, { Component, ErrorInfo, ReactNode } from 'react';

  interface Props {
    children: ReactNode;
  }

  interface State {
    hasError: boolean;
    error: Error | null;
  }

  export class ErrorBoundary extends Component<Props, State> {
    public state: State = {
      hasError: false,
      error: null
    };

    public static getDerivedStateFromError(error: Error): State {
      return { hasError: true, error };
    }

    public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
      console.error('Uncaught error:', error, errorInfo);
    }

    public render() {
      if (this.state.hasError) {
        return (
          <div className="min-h-screen bg-[#0F172A] flex items-center justify-center p-4">
            <div className="bg-[#1E293B] border-2 border-[#EF4444] rounded-xl p-8 max-w-lg shadow-2xl">
              <div className="flex items-center gap-3 mb-4">
                <span className="text-4xl">⚠️ </span>
                <h1 className="text-2xl font-bold text-[#EF4444]">
                  Application Error
                </h1>
              </div>
              <p className="text-[#94A3B8] mb-6 leading-relaxed">
                Something went wrong. Please refresh the page to continue.
              </p>
              <button
                onClick={() => window.location.reload()}
                className="w-full bg-gradient-to-r from-[#667EEA] to-[#764BA2] hover:from-[#5568D3]
  hover:to-[#6941A5] text-white px-6 py-3 rounded-lg font-semibold transition-all duration-300 shadow-lg
  hover:shadow-xl"
              >
                Reload Application
              </button>
            </div>
          </div>
        );
      }

      return this.props.children;
    }
  }