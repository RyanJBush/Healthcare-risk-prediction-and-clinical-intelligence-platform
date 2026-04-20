type PageHeaderProps = {
  title: string;
  subtitle: string;
};

export default function PageHeader({ title, subtitle }: PageHeaderProps) {
  return (
    <header>
      <h2>{title}</h2>
      <p>{subtitle}</p>
    </header>
  );
}
