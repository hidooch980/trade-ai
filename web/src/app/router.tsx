import {
  useCallback,
  useEffect,
  useState,
  type CSSProperties,
  type MouseEvent,
  type ReactNode,
} from "react";

/**
 * Hash routing keeps the site deployable as static files behind any server
 * (including `vite preview` and the FastAPI static mount) with no rewrite rules.
 */

function currentPath(): string {
  const raw = window.location.hash.replace(/^#/, "");
  return raw === "" ? "/" : raw;
}

export function useRoute(): [string, (to: string) => void] {
  const [path, setPath] = useState(currentPath);

  useEffect(() => {
    const onChange = () => setPath(currentPath());
    window.addEventListener("hashchange", onChange);
    return () => window.removeEventListener("hashchange", onChange);
  }, []);

  const navigate = useCallback((to: string) => {
    if (to.startsWith("#")) to = to.slice(1);
    window.location.hash = to;
  }, []);

  return [path, navigate];
}

export function navigate(to: string) {
  window.location.hash = to.startsWith("#") ? to.slice(1) : to;
}

interface LinkProps {
  to: string;
  children: ReactNode;
  className?: string;
  onClick?: () => void;
  ariaLabel?: string;
  style?: CSSProperties;
}

export function Link({ to, children, className, onClick, ariaLabel, style }: LinkProps) {
  const handle = (e: MouseEvent<HTMLAnchorElement>) => {
    // External links and in-page anchors keep native behaviour.
    if (to.startsWith("http")) return;
    e.preventDefault();
    onClick?.();
    if (to.includes("#") && !to.startsWith("/")) {
      document.querySelector(to)?.scrollIntoView({ behavior: "smooth" });
      return;
    }
    navigate(to);
    window.scrollTo({ top: 0, behavior: "instant" as ScrollBehavior });
  };

  return (
    <a
      href={to.startsWith("http") ? to : `#${to}`}
      className={className}
      style={style}
      onClick={handle}
      aria-label={ariaLabel}
      {...(to.startsWith("http") ? { target: "_blank", rel: "noreferrer noopener" } : {})}
    >
      {children}
    </a>
  );
}
