import Image from "next/image";
export default function Page() {
    return <div>
            <p>CUSTOMER is the best</p>
            <Image
            src= "/hero-desktop.png"
            width={1000}
            height={750}
            alt="tester"/>
        </div>;
}