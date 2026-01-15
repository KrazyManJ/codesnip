import { LucideCode2 } from "lucide-react";


const Banner = () => {
    return (
        <div className="my-8">
            <h1 className="flex gap-2 items-center justify-center my-6">
                <LucideCode2 size={64}/>
                <span className="text-5xl font-bold">
                    <span className="font-mono decoration-amber-400 decoration-wavy underline">Code</span>
                    <span className="text-amber-400">Snip</span>
                </span>
            </h1>
            <div className="text-center text-sm">Share and re-use snippets in your code to speed up your workflow!</div>
        </div>
    );
};

export default Banner;
