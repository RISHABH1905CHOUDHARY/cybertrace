import { NextResponse } from "next/server";

export function middleware(request) {
  const loggedIn = request.cookies.get("loggedIn")?.value;

  if (loggedIn !== "true") {
    return NextResponse.redirect(
      new URL("/login", request.url)
    );
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/",
    "/predictions/:path*",
    "/alerts/:path*",
    "/complaints/:path*",
    "/analytics/:path*",
    "/reports/:path*",
    "/settings/:path*",
  ],
};