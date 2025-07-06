import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  // Temporarily disabled authentication middleware
  // TODO: Implement proper auth integration
  
  return NextResponse.next()
}

export const config = {
  matcher: [
    // Only run on dashboard routes for now
    '/dashboard/:path*',
  ]
}
