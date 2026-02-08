import { useEffect, useRef } from 'react';

const GiscusComments = ({ lang = 'zh' }) => {
  const containerRef = useRef(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Remove existing giscus iframe if any
    const existingScript = containerRef.current.querySelector('.giscus');
    if (existingScript) existingScript.remove();
    const existingScriptTag = containerRef.current.querySelector('script');
    if (existingScriptTag) existingScriptTag.remove();

    const script = document.createElement('script');
    script.src = 'https://giscus.app/client.js';
    // TODO: After enabling GitHub Discussions on the repo, update these values
    // Visit https://giscus.app/ to generate the correct data-repo-id and data-category-id
    script.setAttribute('data-repo', 'beihaili/Stories-about-Bitcoin');
    script.setAttribute('data-repo-id', 'R_kgDOPnWv-w');
    script.setAttribute('data-category', 'Announcements');
    script.setAttribute('data-category-id', 'DIC_kwDOPnWv-84C2Btd');
    script.setAttribute('data-mapping', 'pathname');
    script.setAttribute('data-strict', '1');
    script.setAttribute('data-reactions-enabled', '1');
    script.setAttribute('data-emit-metadata', '0');
    script.setAttribute('data-input-position', 'top');
    script.setAttribute('data-theme', 'light');
    script.setAttribute('data-lang', lang === 'zh' ? 'zh-CN' : 'en');
    script.setAttribute('data-loading', 'lazy');
    script.setAttribute('crossorigin', 'anonymous');
    script.async = true;

    containerRef.current.appendChild(script);
  }, [lang]);

  const content = {
    zh: {
      title: '读者讨论区',
      subtitle: '基于 GitHub Discussions，登录 GitHub 即可参与讨论',
    },
    en: {
      title: 'Reader Discussions',
      subtitle: 'Powered by GitHub Discussions. Sign in with GitHub to comment.',
    }
  };

  const t = content[lang];

  return (
    <section className="bg-historical-parchment py-16 sm:py-20">
      <div className="max-w-4xl mx-auto px-4 sm:px-6">
        <div className="text-center mb-8">
          <h2 className="text-3xl sm:text-4xl font-bold text-historical-sepia mb-3">
            {t.title}
          </h2>
          <p className="text-historical-antique">
            {t.subtitle}
          </p>
        </div>
        <div ref={containerRef} className="giscus-container" />
      </div>
    </section>
  );
};

export default GiscusComments;
