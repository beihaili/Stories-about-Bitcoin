import { motion } from 'framer-motion';
import { FaGithub, FaTwitter, FaBook, FaHeart, FaBitcoin, FaRss } from 'react-icons/fa';
import ShareButtons from './ShareButtons';

const Footer = ({ lang = 'zh' }) => {
  const content = {
    zh: {
      title: '比特币那些事儿',
      subtitle: '以网文笔法讲比特币的故事',
      description: '一部用《明朝那些事儿》风格讲述比特币历史的开源双语电子书',
      readNow: '立即阅读',
      quickLinks: '快速链接',
      chapters: '章节目录',
      timeline: '时间线',
      figures: '关键人物',
      connect: '关注我们',
      openSource: '开源项目',
      license: 'MIT 许可证',
      madeWith: '用心制作',
      copyright: '© 2024 Stories about Bitcoin',
    },
    en: {
      title: 'Stories about Bitcoin',
      subtitle: 'Bitcoin History in Web Novel Style',
      description: 'An open-source bilingual ebook telling Bitcoin history in the style of "Those Things in Ming Dynasty"',
      readNow: 'Read Now',
      quickLinks: 'Quick Links',
      chapters: 'Chapters',
      timeline: 'Timeline',
      figures: 'Key Figures',
      connect: 'Connect',
      openSource: 'Open Source',
      license: 'MIT License',
      madeWith: 'Made with',
      copyright: '© 2024 Stories about Bitcoin',
    }
  };

  const t = content[lang];

  const scrollToSection = (id) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <footer className="bg-gradient-to-b from-historical-sepia to-[#5a3510] text-bitcoin-lightGold">
      {/* Main Footer Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-12 sm:py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 lg:gap-12">
          {/* Brand Column */}
          <div className="col-span-1 md:col-span-2 lg:col-span-1">
            <motion.div
              className="flex items-center gap-3 mb-4"
              whileHover={{ scale: 1.02 }}
            >
              <FaBitcoin className="text-3xl text-bitcoin-orange" />
              <h3 className="text-xl font-bold">{t.title}</h3>
            </motion.div>
            <p className="text-sm opacity-80 mb-4 leading-relaxed">
              {t.description}
            </p>
            <a
              href={`https://beihaili.github.io/Stories-about-Bitcoin/${lang}/`}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 bg-bitcoin-orange hover:bg-bitcoin-gold text-white font-semibold py-2 px-4 rounded-lg transition-colors"
            >
              <FaBook />
              {t.readNow}
            </a>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-lg font-semibold mb-4 text-white">{t.quickLinks}</h4>
            <ul className="space-y-2">
              <li>
                <button
                  onClick={() => scrollToSection('chapters')}
                  className="text-sm opacity-80 hover:opacity-100 hover:text-bitcoin-orange transition-all"
                >
                  {t.chapters}
                </button>
              </li>
              <li>
                <button
                  onClick={() => scrollToSection('timeline')}
                  className="text-sm opacity-80 hover:opacity-100 hover:text-bitcoin-orange transition-all"
                >
                  {t.timeline}
                </button>
              </li>
              <li>
                <button
                  onClick={() => scrollToSection('figures')}
                  className="text-sm opacity-80 hover:opacity-100 hover:text-bitcoin-orange transition-all"
                >
                  {t.figures}
                </button>
              </li>
            </ul>
          </div>

          {/* Connect */}
          <div>
            <h4 className="text-lg font-semibold mb-4 text-white">{t.connect}</h4>
            <div className="flex flex-col gap-3">
              <a
                href="https://github.com/beihaili/Stories-about-Bitcoin"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-3 text-sm opacity-80 hover:opacity-100 hover:text-bitcoin-orange transition-all"
              >
                <FaGithub className="text-lg" />
                GitHub
              </a>
              <a
                href="https://twitter.com/bhbtc1337"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-3 text-sm opacity-80 hover:opacity-100 hover:text-bitcoin-orange transition-all"
              >
                <FaTwitter className="text-lg" />
                Twitter
              </a>
            </div>
          </div>

          {/* Share & Open Source */}
          <div>
            <h4 className="text-lg font-semibold mb-4 text-white">
              {lang === 'zh' ? '分享本书' : 'Share This Book'}
            </h4>
            <div className="mb-4">
              <ShareButtons lang={lang} />
            </div>
            <a
              href="/Stories-about-Bitcoin/feed.xml"
              className="inline-flex items-center gap-2 text-sm opacity-80 hover:opacity-100 hover:text-bitcoin-orange transition-all"
            >
              <FaRss />
              RSS Feed
            </a>
            <div className="flex items-center gap-2 text-sm opacity-60 mt-3">
              <span>{t.madeWith}</span>
              <FaHeart className="text-red-400" />
              <span>& React | {t.license}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4">
          <div className="flex flex-col sm:flex-row justify-between items-center gap-2 text-xs opacity-60">
            <p>{t.copyright}</p>
            <p>{t.subtitle}</p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
