import { useState } from 'react';
import { motion } from 'framer-motion';
import { FaGithub, FaTwitter, FaBook, FaHeart, FaBitcoin, FaRss, FaBolt, FaCopy, FaCheck, FaQrcode } from 'react-icons/fa';
import { QRCodeSVG } from 'qrcode.react';
import ShareButtons from './ShareButtons';

const BTC_ADDRESS = 'bc1qjt7uhztd2pumpx6p5w0sl8jxfzmxp3nyahysmcqklqfkecqftuysu733ca';
const LIGHTNING_ADDRESS = 'latebrook396888@getalby.com';
const NOSTR_NPUB = 'npub1xk5up2m7egnktyulkwrj5wfyts2gmk3vur95qchwzvvnr9jkkgaqqvxa5t';

const Footer = ({ lang = 'zh' }) => {
  const [showQR, setShowQR] = useState(false);
  const [copied, setCopied] = useState(null); // null | 'btc' | 'ln'

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
      support: '支持项目',
      supportDesc: '如果你喜欢这个故事，请考虑支持一下',
      btcDonate: 'BTC 捐赠',
      lnDonate: 'Lightning 打赏',
      copyAddress: '复制地址',
      copied: '已复制！',
      showQR: '显示二维码',
      hideQR: '隐藏二维码',
      madeWith: '用心制作',
      license: 'MIT 许可证',
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
      support: 'Support',
      supportDesc: 'If you enjoy this story, consider supporting the project',
      btcDonate: 'BTC Donation',
      lnDonate: 'Lightning Tips',
      copyAddress: 'Copy Address',
      copied: 'Copied!',
      showQR: 'Show QR',
      hideQR: 'Hide QR',
      madeWith: 'Made with',
      license: 'MIT License',
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

  const copyToClipboard = async (text, type) => {
    try {
      await navigator.clipboard.writeText(text);
    } catch {
      const textarea = document.createElement('textarea');
      textarea.value = text;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
    }
    setCopied(type);
    setTimeout(() => setCopied(null), 2000);
  };

  const truncatedAddress = `${BTC_ADDRESS.slice(0, 10)}...${BTC_ADDRESS.slice(-6)}`;

  return (
    <footer className="bg-gradient-to-b from-historical-sepia to-[#5a3510] text-bitcoin-lightGold" aria-label={lang === 'zh' ? '页脚导航' : 'Footer navigation'}>
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
                aria-label={lang === 'zh' ? 'Twitter 账号' : 'Twitter account'}
                className="flex items-center gap-3 text-sm opacity-80 hover:opacity-100 hover:text-bitcoin-orange transition-all"
              >
                <FaTwitter className="text-lg" />
                Twitter
              </a>
              <a
                href={`https://njump.me/${NOSTR_NPUB}`}
                target="_blank"
                rel="noopener noreferrer"
                aria-label="Nostr"
                className="flex items-center gap-3 text-sm opacity-80 hover:opacity-100 hover:text-bitcoin-orange transition-all"
              >
                <FaBolt className="text-lg" />
                Nostr
              </a>
            </div>
          </div>

          {/* Support Project */}
          <div>
            <h4 className="text-lg font-semibold mb-4 text-white">{t.support}</h4>
            <p className="text-sm opacity-80 mb-3">{t.supportDesc}</p>

            {/* Lightning Address */}
            <div className="bg-black/20 rounded-lg p-3 mb-2">
              <div className="flex items-center gap-2 mb-1">
                <FaBolt className="text-yellow-400 text-sm" />
                <span className="text-xs font-semibold text-yellow-400">{t.lnDonate}</span>
              </div>
              <div className="flex items-center gap-2">
                <code className="text-xs opacity-90 flex-1 break-all">{LIGHTNING_ADDRESS}</code>
                <button
                  onClick={() => copyToClipboard(LIGHTNING_ADDRESS, 'ln')}
                  className="text-sm hover:text-bitcoin-orange transition-colors p-1"
                  title={copied === 'ln' ? t.copied : t.copyAddress}
                >
                  {copied === 'ln' ? <FaCheck className="text-green-400" /> : <FaCopy />}
                </button>
              </div>
            </div>

            {/* BTC Address */}
            <div className="bg-black/20 rounded-lg p-3 mb-3">
              <div className="flex items-center gap-2 mb-1">
                <FaBitcoin className="text-bitcoin-orange text-sm" />
                <span className="text-xs font-semibold text-bitcoin-orange">{t.btcDonate}</span>
              </div>
              <div className="flex items-center gap-2">
                <code className="text-xs opacity-90 flex-1">{truncatedAddress}</code>
                <button
                  onClick={() => copyToClipboard(BTC_ADDRESS, 'btc')}
                  className="text-sm hover:text-bitcoin-orange transition-colors p-1"
                  title={copied === 'btc' ? t.copied : t.copyAddress}
                >
                  {copied === 'btc' ? <FaCheck className="text-green-400" /> : <FaCopy />}
                </button>
                <button
                  onClick={() => setShowQR(!showQR)}
                  className="text-sm hover:text-bitcoin-orange transition-colors p-1"
                  title={showQR ? t.hideQR : t.showQR}
                >
                  <FaQrcode />
                </button>
              </div>
              {showQR && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  className="mt-3 flex justify-center"
                >
                  <div className="bg-white p-2 rounded-lg">
                    <QRCodeSVG
                      value={`bitcoin:${BTC_ADDRESS}`}
                      size={120}
                      bgColor="#ffffff"
                      fgColor="#000000"
                    />
                  </div>
                </motion.div>
              )}
            </div>

            {/* Share & RSS */}
            <div className="mt-3">
              <ShareButtons lang={lang} />
            </div>
            <a
              href="/Stories-about-Bitcoin/feed.xml"
              className="inline-flex items-center gap-2 text-xs opacity-60 hover:opacity-100 hover:text-bitcoin-orange transition-all mt-2"
            >
              <FaRss /> RSS
            </a>
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4">
          <div className="flex flex-col sm:flex-row justify-between items-center gap-2 text-xs opacity-60">
            <p>{t.copyright}</p>
            <div className="flex items-center gap-1">
              <span>{t.madeWith}</span>
              <FaHeart className="text-red-400" />
              <span>& React | {t.license}</span>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
