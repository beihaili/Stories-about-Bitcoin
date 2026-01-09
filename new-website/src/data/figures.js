// 比特币那些事儿 - 关键人物数据
export const figures = [
  {
    id: 'hayek',
    name: {
      zh: '弗里德里希·哈耶克',
      en: 'Friedrich Hayek'
    },
    role: {
      zh: '货币理论先驱',
      en: 'Monetary Theory Pioneer'
    },
    years: '1899-1992',
    image: '/assets/figures/hayek.jpg',
    description: {
      zh: '诺贝尔经济学奖得主，《货币的非国家化》作者，预言了私人货币的可能性',
      en: 'Nobel Prize in Economics, author of "Denationalisation of Money", prophesied private currency'
    },
    contributions: {
      zh: ['提出私人货币竞争理论', '批判中央银行垄断', '奠定比特币哲学基础'],
      en: ['Proposed private currency competition theory', 'Criticized central bank monopoly', 'Laid philosophical foundation for Bitcoin']
    },
    quote: {
      zh: '我不相信我们会找到一个好的货币，除非我们把它从政府手中拿走。',
      en: 'I don\'t believe we shall ever have a good money again before we take it out of the hands of government.'
    }
  },
  {
    id: 'chaum',
    name: {
      zh: '大卫·乔姆',
      en: 'David Chaum'
    },
    role: {
      zh: '数字现金之父',
      en: 'Father of Digital Cash'
    },
    years: '1955-',
    image: '/assets/figures/chaum.jpg',
    description: {
      zh: '密码学家，DigiCash创始人，首个数字货币eCash发明者',
      en: 'Cryptographer, DigiCash founder, inventor of first digital currency eCash'
    },
    contributions: {
      zh: ['发明盲签名技术', '创建首个数字货币系统', '开创密码学货币先河'],
      en: ['Invented blind signature', 'Created first digital currency system', 'Pioneered cryptographic currency']
    },
    quote: {
      zh: '隐私不是秘密。隐私是你不想让全世界知道的东西，秘密是你不想让任何人知道的东西。',
      en: 'Privacy is not secrecy. Privacy is something you don\'t want the whole world to know, secrecy is something you don\'t want anybody to know.'
    }
  },
  {
    id: 'satoshi',
    name: {
      zh: '中本聪',
      en: 'Satoshi Nakamoto'
    },
    role: {
      zh: '比特币创造者',
      en: 'Bitcoin Creator'
    },
    years: '?-?',
    image: '/assets/figures/satoshi.jpg',
    description: {
      zh: '身份未知的传奇人物，比特币白皮书作者，比特币网络创建者',
      en: 'Legendary figure of unknown identity, Bitcoin whitepaper author, Bitcoin network creator'
    },
    contributions: {
      zh: ['发布比特币白皮书', '启动比特币网络', '解决双花问题', '创造区块链技术'],
      en: ['Published Bitcoin whitepaper', 'Launched Bitcoin network', 'Solved double-spending problem', 'Created blockchain technology']
    },
    quote: {
      zh: '根深蒂固的问题在于：要让基于法定货币的系统运作，就必须信任中央银行不会让货币贬值。',
      en: 'The root problem with conventional currency is all the trust that\'s required to make it work.'
    }
  },
  {
    id: 'hal-finney',
    name: {
      zh: '哈尔·芬尼',
      en: 'Hal Finney'
    },
    role: {
      zh: '第一个信徒',
      en: 'First Believer'
    },
    years: '1956-2014',
    image: '/assets/figures/hal.jpg',
    description: {
      zh: '密码学家，第一个比特币接收者，比特币早期开发者',
      en: 'Cryptographer, first Bitcoin recipient, early Bitcoin developer'
    },
    contributions: {
      zh: ['接收第一笔比特币交易', 'RPOW系统创建者', '比特币代码优化', '坚定的早期支持者'],
      en: ['Received first Bitcoin transaction', 'Creator of RPOW system', 'Bitcoin code optimization', 'Steadfast early supporter']
    },
    quote: {
      zh: '我看到的不是玻璃杯半空，而是半满。',
      en: 'I see the glass as half full, not half empty.'
    }
  },
  {
    id: 'gavin',
    name: {
      zh: '加文·安德烈森',
      en: 'Gavin Andresen'
    },
    role: {
      zh: '首席开发者',
      en: 'Lead Developer'
    },
    years: '1966-',
    image: '/assets/figures/gavin.jpg',
    description: {
      zh: '中本聪退出后的比特币首席开发者，推动比特币主流化',
      en: 'Lead Bitcoin developer after Satoshi\'s departure, promoted Bitcoin mainstream adoption'
    },
    contributions: {
      zh: ['接管比特币核心开发', '建立比特币基金会', '推动与监管机构对话', '改进比特币代码库'],
      en: ['Took over Bitcoin core development', 'Established Bitcoin Foundation', 'Promoted dialogue with regulators', 'Improved Bitcoin codebase']
    },
    quote: {
      zh: '比特币将改变世界，或者它将失败。没有中间地带。',
      en: 'Bitcoin will change the world, or it will fail. There is no middle ground.'
    }
  },
  {
    id: 'roger-ver',
    name: {
      zh: '罗杰·沃',
      en: 'Roger Ver'
    },
    role: {
      zh: '比特币耶稣',
      en: 'Bitcoin Jesus'
    },
    years: '1979-',
    image: '/assets/figures/roger.jpg',
    description: {
      zh: '早期投资者和布道者，推动比特币商业应用',
      en: 'Early investor and evangelist, promoted Bitcoin business applications'
    },
    contributions: {
      zh: ['早期大量投资比特币', '资助比特币初创公司', '推广比特币支付', '比特币现金支持者'],
      en: ['Heavy early Bitcoin investment', 'Funded Bitcoin startups', 'Promoted Bitcoin payments', 'Bitcoin Cash supporter']
    },
    quote: {
      zh: '比特币是人类有史以来最重要的发明之一。',
      en: 'Bitcoin is one of the most important inventions in all of human history.'
    }
  },
  {
    id: 'ross-ulbricht',
    name: {
      zh: '罗斯·乌布利希',
      en: 'Ross Ulbricht'
    },
    role: {
      zh: '丝绸之路创始人',
      en: 'Silk Road Founder'
    },
    years: '1984-',
    image: '/assets/figures/ross.jpg',
    description: {
      zh: '暗网市场"丝绸之路"创建者，自由主义信仰者',
      en: 'Creator of darknet marketplace "Silk Road", libertarian believer'
    },
    contributions: {
      zh: ['创建第一个大规模比特币使用场景', '证明比特币的实用性', '引发关于自由的辩论'],
      en: ['Created first large-scale Bitcoin use case', 'Proved Bitcoin\'s practicality', 'Sparked debate about freedom']
    },
    quote: {
      zh: '丝绸之路是关于自由的，是关于人们有权做出自己选择的。',
      en: 'Silk Road was about freedom, it was about people having the right to make their own choices.'
    }
  },
  {
    id: 'winklevoss',
    name: {
      zh: '温克莱沃斯兄弟',
      en: 'Winklevoss Twins'
    },
    role: {
      zh: '机构投资先驱',
      en: 'Institutional Investment Pioneers'
    },
    years: '1981-',
    image: '/assets/figures/winklevoss.jpg',
    description: {
      zh: 'Facebook早期投资者，Gemini交易所创始人',
      en: 'Early Facebook investors, Gemini exchange founders'
    },
    contributions: {
      zh: ['大量购买比特币', '创建合规交易所Gemini', '推动比特币ETF', '连接华尔街与加密货币'],
      en: ['Heavy Bitcoin purchases', 'Created compliant exchange Gemini', 'Promoted Bitcoin ETF', 'Connected Wall Street to crypto']
    },
    quote: {
      zh: '我们认为比特币将比互联网更具颠覆性。',
      en: 'We believe Bitcoin will be more disruptive than the Internet.'
    }
  },
  {
    id: 'saylor',
    name: {
      zh: '迈克尔·塞勒',
      en: 'Michael Saylor'
    },
    role: {
      zh: '企业比特币化先驱',
      en: 'Corporate Bitcoin Pioneer'
    },
    years: '1965-',
    image: '/assets/figures/saylor.jpg',
    description: {
      zh: 'MicroStrategy CEO，将比特币作为企业储备资产',
      en: 'MicroStrategy CEO, adopted Bitcoin as corporate treasury asset'
    },
    contributions: {
      zh: ['公司购买数十亿美元比特币', '推动企业采用比特币', '比特币教育布道', '影响其他企业跟进'],
      en: ['Company purchased billions in Bitcoin', 'Promoted corporate Bitcoin adoption', 'Bitcoin education evangelism', 'Influenced other companies to follow']
    },
    quote: {
      zh: '比特币是一个由天才为所有人建造的防御网络。',
      en: 'Bitcoin is a swarm of cyber hornets serving the goddess of wisdom, feeding on the fire of truth.'
    }
  },
  {
    id: 'bukele',
    name: {
      zh: '纳伊布·布克尔',
      en: 'Nayib Bukele'
    },
    role: {
      zh: '比特币法币化先驱',
      en: 'Bitcoin Legal Tender Pioneer'
    },
    years: '1981-',
    image: '/assets/figures/bukele.jpg',
    description: {
      zh: '萨尔瓦多总统，推动比特币成为法定货币',
      en: 'President of El Salvador, promoted Bitcoin as legal tender'
    },
    contributions: {
      zh: ['使比特币成为萨尔瓦多法币', '建设比特币城市', '国家级比特币储备', '开创国家采用先例'],
      en: ['Made Bitcoin legal tender in El Salvador', 'Building Bitcoin City', 'National Bitcoin reserves', 'Pioneered national adoption']
    },
    quote: {
      zh: '这不仅仅是关于比特币，而是关于自由。',
      en: 'This is not just about Bitcoin, it\'s about freedom.'
    }
  }
];

// 根据ID获取人物
export const getFigureById = (id) => {
  return figures.find(figure => figure.id === id);
};

// 获取所有人物名字列表
export const getFigureNames = (lang = 'zh') => {
  return figures.map(f => f.name[lang]);
};
