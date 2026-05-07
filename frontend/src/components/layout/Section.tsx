interface SectionProps {
  id: string;
  className?: string;
  children: React.ReactNode;
}

export function Section({ id, className = "", children }: SectionProps) {
  return (
    <section id={id} className={`section ${className}`.trim()}>
      <div className="section__inner">{children}</div>
    </section>
  );
}
