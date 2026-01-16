import { 
  SiGnubash, SiCplusplus, SiCss3, SiDart, SiElixir, SiGo, 
  SiGraphql, SiApachegroovy, SiHaskell, SiTerraform, SiHtml5, 
  SiJavascript, SiJson, SiKotlin, SiLua, SiNginx, SiPerl, 
  SiPhp, SiPrometheus, SiPython, SiR, SiRedis, 
  SiRuby, SiSwift, SiTypescript, SiYaml 
} from "react-icons/si";
import { TbBrandCSharp, TbSql } from "react-icons/tb";
import { FaJava } from "react-icons/fa";
import { 
  LucideFileCode, LucideFileText, LucideTerminal, LucideFileCog 
} from "lucide-react";
import { VscTerminalPowershell } from "react-icons/vsc";

interface LanguageIconProps {
    language: string;
    className?: string;
    size?: number;
}

export const LanguageIcon = ({ language, className, size = 16 }: LanguageIconProps) => {
    const lang = language.toLowerCase();

    const iconMap: Record<string, React.ElementType> = {
        bash: SiGnubash,
        batch: LucideTerminal,
        cpp: SiCplusplus,
        csharp: TbBrandCSharp,
        css: SiCss3,
        dart: SiDart,
        elixir: SiElixir,
        go: SiGo,
        graphql: SiGraphql,
        groovy: SiApachegroovy,
        haskell: SiHaskell,
        hcl: SiTerraform,
        html: SiHtml5,
        java: FaJava,
        javascript: SiJavascript,
        json: SiJson,
        kotlin: SiKotlin,
        lua: SiLua,
        makefile: LucideFileCog,
        nginx: SiNginx,
        perl: SiPerl,
        php: SiPhp,
        powershell: VscTerminalPowershell,
        promql: SiPrometheus, 
        python: SiPython,
        r: SiR,
        redis: SiRedis,
        ruby: SiRuby,
        sql: TbSql,
        swift: SiSwift,
        text: LucideFileText,
        typescript: SiTypescript,
        yaml: SiYaml,
    };

    const IconComponent = iconMap[lang] || LucideFileCode;

    return <IconComponent className={className} size={size}/>;
};
