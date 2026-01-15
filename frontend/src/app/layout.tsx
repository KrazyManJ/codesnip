import type { Metadata } from "next";
import "./globals.css";
import { Providers } from "@/providers";

import { JetBrains_Mono, Inter } from "next/font/google";
import Header from "@/components/Header";

const inter = Inter({
    subsets: ["latin"],
    display: "swap",
    variable: "--font-sans",
});

const jetBrainsMono = JetBrains_Mono({
    subsets: ["latin"],
    display: "swap",
    variable: "--font-mono",
});

export const metadata: Metadata = {
    title: "CodeSnip"
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en" suppressHydrationWarning>
            <body className={`${inter.variable} ${jetBrainsMono.variable} antialiased min-h-screen`}>
                <Providers>
                    <Header/>
                    <div className="max-w-7xl mx-auto p-4">
                        {children}
                    </div>
                </Providers>
            </body>
        </html>
    );
}
