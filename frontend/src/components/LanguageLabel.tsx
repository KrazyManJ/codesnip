interface LanguageLabelProps {
  language: string;
}

export const LanguageLabel = ({ language }: LanguageLabelProps) => {
    const lang = language.toLowerCase();

    const labelMap: Record<string, string> = {
        bash: "Bash",
        batch: "Batch Script",
        cpp: "C++",
        csharp: "C#",
        css: "CSS",
        dart: "Dart",
        elixir: "Elixir",
        go: "Go",
        graphql: "GraphQL",
        groovy: "Groovy",
        haskell: "Haskell",
        hcl: "Terraform (HCL)",
        html: "HTML",
        java: "Java",
        javascript: "JavaScript",
        json: "JSON",
        kotlin: "Kotlin",
        lua: "Lua",
        makefile: "Makefile",
        nginx: "Nginx",
        perl: "Perl",
        php: "PHP",
        powershell: "PowerShell",
        promql: "PromQL",
        python: "Python",
        r: "R Language",
        redis: "Redis",
        ruby: "Ruby",
        sql: "SQL",
        swift: "Swift",
        text: "Plain Text",
        typescript: "TypeScript",
        yaml: "YAML",
    };

    const displayName =
        labelMap[lang] || language.charAt(0).toUpperCase() + language.slice(1);

    return <>{displayName}</>;
};
