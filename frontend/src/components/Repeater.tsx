import React, { ReactNode } from "react";

interface RepeaterProps {
    children: ReactNode
    n: number
}


const Repeater = ({children,n }: RepeaterProps) => {
    return (
        <>
            {new Array(n).fill(0).map(() => children)}
        </>
    );
};

export default Repeater;
