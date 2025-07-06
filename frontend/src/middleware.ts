import { withAuth } from 'next-auth/middleware'

export default withAuth(
  function middleware(req) {
    // Add any additional middleware logic here
  },
  {
    callbacks: {
      authorized: ({ token, req }) => {
        // Check if user is trying to access protected routes
        if (req.nextUrl.pathname.startsWith('/dashboard')) {
          return !!token
        }
        
        // Allow access to public routes
        return true
      },
    },
  }
)

export const config = {
  matcher: [
    // Protect these routes
    '/dashboard/:path*',
    '/profile/:path*',
    '/settings/:path*',
    // Don't run middleware on these paths
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ]
}
