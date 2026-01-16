import { useEffect, useRef } from "react";


export default function useIsMounter() {
    const mounted = useRef<boolean>(false)
    useEffect(() => {mounted.current = true}, [])
    return () => mounted.current
}