import { auth } from '@/lib/auth/config'
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  const session = await auth()
  
  // Check if user is trying to access protected routes
  if (request.nextUrl.pathname.startsWith('/dashboard')) {
    if (!session) {
      return NextResponse.redirect(new URL('/login', request.url))
    }
  }
  
  return NextResponse.next()
}

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
