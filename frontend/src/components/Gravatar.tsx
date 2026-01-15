import Image from "next/image";
import md5 from "crypto-js/md5";

type GravatarProps = {
    size?: number;
    className?: string;
} & ({
    email: string;
} | {
    emailHash: string;
});

const Gravatar = (props: GravatarProps) => {

    const { size, className } = props

    const hash = "emailHash" in props ? props.emailHash : md5(props.email.trim().toLowerCase());

    const url = `https://www.gravatar.com/avatar/${hash}?s=${size}&d=identicon`;

    return (
        <div className={`rounded-full overflow-hidden ${className}`}>
            <Image
                src={url}
                alt={hash}
                width={size}
                height={size}
            />
        </div>
    );
};

export default Gravatar;
