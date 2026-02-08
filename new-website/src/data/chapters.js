// 比特币那些事儿 - 章节数据
export const periods = [
  {
    id: 'prologue',
    name: { zh: '序言', en: 'Prologue' },
    years: '',
    description: { zh: '理想与现实的序章', en: 'Prelude to Ideals and Reality' }
  },
  {
    id: 'genesis',
    name: { zh: '创世纪', en: 'Genesis' },
    years: '1976-2009',
    description: { zh: '从理论到实践的伟大跨越', en: 'The Great Leap from Theory to Practice' }
  },
  {
    id: 'first-steps',
    name: { zh: '初出茅庐', en: 'First Steps' },
    years: '2009-2010',
    description: { zh: '新生事物的艰难起步', en: 'The Difficult Beginnings of Something New' }
  },
  {
    id: 'rising-storm',
    name: { zh: '风起云涌', en: 'Rising Storm' },
    years: '2011-2012',
    description: { zh: '走向公众视野', en: 'Coming into Public View' }
  },
  {
    id: 'undercurrents',
    name: { zh: '暗潮汹涌', en: 'Undercurrents' },
    years: '2013-2015',
    description: { zh: '监管与自由的博弈', en: 'The Struggle Between Regulation and Freedom' }
  },
  {
    id: 'breaking-waves',
    name: { zh: '破浪前行', en: 'Breaking Waves' },
    years: '2016-2020',
    description: { zh: '迈向主流的征程', en: 'Journey Towards Mainstream' }
  },
  {
    id: 'future-promise',
    name: { zh: '未来可期', en: 'Future Promise' },
    years: '2021-2024',
    description: { zh: '走向全球储备货币', en: 'Towards Global Reserve Currency' }
  },
  {
    id: 'special',
    name: { zh: '特别篇', en: 'Special' },
    years: '',
    description: { zh: '致敬先驱', en: 'Tribute to Pioneers' }
  }
];

export const chapters = [
  // 序言
  {
    id: 0,
    period: 'prologue',
    title: {
      zh: '引子：一束照进现实的理想之光',
      en: 'Prologue: A Beam of Idealism Illuminating Reality'
    },
    icon: '📖',
    summary: {
      zh: '理想与现实的思辨，比特币的哲学意义',
      en: 'Philosophical Reflections on Ideals vs Reality'
    },
    image: 'img/00.png',
    link: { zh: '/zh/00_引子：一束照进现实的理想之光.html', en: '/en/00_introduction_beam_of_idealistic_light.html' },
    year: '',
    readingTime: 5
  },

  // 创世纪 (1976-2009)
  {
    id: 1,
    period: 'genesis',
    title: {
      zh: '创世纪：穿越时空的\u201c神级反杀\u201d',
      en: 'Genesis: Hayek\'s Prophecy'
    },
    icon: '🔮',
    summary: {
      zh: '货币理论基础，私人货币的设想',
      en: 'Monetary Theory Foundation, Vision of Private Currency'
    },
    image: 'img/01.png',
    link: { zh: '/zh/01_创世纪：穿越时空的\u201c神级反杀\u201d.html', en: '/en/01_genesis_hayeks_prophecy.html' },
    year: '1976',
    readingTime: 6
  },
  {
    id: 2,
    period: 'genesis',
    title: {
      zh: '创世纪：乔姆的孤独方舟',
      en: 'Genesis: Chaum\'s Lonely Ark'
    },
    icon: '⛵',
    summary: {
      zh: '数字现金先驱，密码学货币雏形',
      en: 'Digital Cash Pioneer, Cryptographic Currency Prototype'
    },
    image: 'img/02.png',
    link: { zh: '/zh/02_创世纪：乔姆的孤独方舟.html', en: '/en/02_genesis_chaums_lonely_ark.html' },
    year: '1982',
    readingTime: 5
  },
  {
    id: 3,
    period: 'genesis',
    title: {
      zh: '创世纪：密码朋克的技术拼图',
      en: 'Genesis: The Cypherpunk Technology Puzzle'
    },
    icon: '🧩',
    summary: {
      zh: '技术积累，密码朋克运动',
      en: 'Technical Accumulation, Cypherpunk Movement'
    },
    image: 'img/03.png',
    link: { zh: '/zh/03_创世纪：密码朋克的技术拼图.html', en: '/en/03_genesis_cypherpunk_technical_puzzle.html' },
    year: '1990s',
    readingTime: 11
  },
  {
    id: 4,
    period: 'genesis',
    title: {
      zh: '创世纪：08年发生了什么',
      en: 'Genesis: What Happened in 2008'
    },
    icon: '⏰',
    summary: {
      zh: '金融危机背景，时代契机',
      en: 'Financial Crisis Background, Historical Opportunity'
    },
    image: 'img/04.png',
    link: { zh: '/zh/04_创世纪：08年发生了什么.html', en: '/en/04_genesis_what_happened_in_2008.html' },
    year: '2008',
    readingTime: 10
  },
  {
    id: 5,
    period: 'genesis',
    title: {
      zh: '创世纪：中本聪创世',
      en: 'Genesis: Satoshi\'s Genesis'
    },
    icon: '🎯',
    summary: {
      zh: '比特币诞生，白皮书发布',
      en: 'Bitcoin Birth, Whitepaper Published'
    },
    image: 'img/05.png',
    link: { zh: '/zh/05_创世纪：中本聪创世.html', en: '/en/05_genesis_satoshis_genesis.html' },
    year: '2009',
    readingTime: 9
  },

  // 初出茅庐 (2009-2010)
  {
    id: 6,
    period: 'first-steps',
    title: {
      zh: '初出茅庐：第一个信徒',
      en: 'First Steps: The First Believer'
    },
    icon: '👤',
    summary: {
      zh: '哈尔·芬尼的传承故事',
      en: 'Hal Finney\'s Legacy Story'
    },
    image: 'img/06.png',
    link: { zh: '/zh/06_初出茅庐：第一个信徒.html', en: '/en/06_first_steps_first_believer.html' },
    year: '2009',
    readingTime: 14
  },
  {
    id: 7,
    period: 'first-steps',
    title: {
      zh: '初出茅庐：社区与工具',
      en: 'First Steps: Community and Tools'
    },
    icon: '🛠️',
    summary: {
      zh: 'BitcoinTalk论坛与工具生态',
      en: 'BitcoinTalk Forum and Tool Ecosystem'
    },
    image: 'img/07.png',
    link: { zh: '/zh/07_初出茅庐：社区与工具.html', en: '/en/07_first_steps_community_and_tools.html' },
    year: '2009',
    readingTime: 7
  },
  {
    id: 8,
    period: 'first-steps',
    title: {
      zh: '初出茅庐：价值发现',
      en: 'First Steps: Value Discovery'
    },
    icon: '💰',
    summary: {
      zh: '从无价到有价的历史突破',
      en: 'Historic Breakthrough from Priceless to Priced'
    },
    image: 'img/08.png',
    link: { zh: '/zh/08_初出茅庐：价值发现.html', en: '/en/08_first_steps_value_discovery.html' },
    year: '2010',
    readingTime: 13
  },
  {
    id: 9,
    period: 'first-steps',
    title: {
      zh: '初出茅庐：第一次危机与修复',
      en: 'First Steps: First Crisis and Recovery'
    },
    icon: '🔧',
    summary: {
      zh: '史上最大胆的网络回滚',
      en: 'The Most Daring Network Rollback in History'
    },
    image: 'img/09.png',
    link: { zh: '/zh/09_初出茅庐：第一次危机与修复.html', en: '/en/09_first_steps_first_crisis_and_fix.html' },
    year: '2010',
    readingTime: 13
  },
  {
    id: 10,
    period: 'first-steps',
    title: {
      zh: '初出茅庐：中本聪的神秘退场',
      en: 'First Steps: Satoshi\'s Mysterious Departure'
    },
    icon: '👻',
    summary: {
      zh: '数字时代最伟大的退场',
      en: 'The Greatest Exit in the Digital Age'
    },
    image: 'img/10.png',
    link: { zh: '/zh/10_初出茅庐：中本聪的神秘退场.html', en: '/en/10_first_steps_satoshis_mysterious_exit.html' },
    year: '2010',
    readingTime: 10
  },

  // 风起云涌 (2011-2012)
  {
    id: 11,
    period: 'rising-storm',
    title: {
      zh: '风起云涌：理想与现实的第一次碰撞',
      en: 'Rising Storm: First Collision of Ideals and Reality'
    },
    icon: '⚔️',
    summary: {
      zh: '丝绸之路的争议与影响',
      en: 'Silk Road\'s Controversy and Impact'
    },
    image: 'img/11.png',
    link: { zh: '/zh/11_风起云涌：理想与现实的第一次碰撞.html', en: '/en/11_rising_storm_ideals_vs_reality.html' },
    year: '2011',
    readingTime: 9
  },
  {
    id: 12,
    period: 'rising-storm',
    title: {
      zh: '风起云涌：Mt.Gox帝国的崛起',
      en: 'Rising Storm: Rise of the Mt.Gox Empire'
    },
    icon: '🏰',
    summary: {
      zh: '从技术实验到商业帝国',
      en: 'From Technical Experiment to Business Empire'
    },
    image: 'img/12.png',
    link: { zh: '/zh/12_风起云涌：Mt.Gox帝国的崛起.html', en: '/en/12_rising_storm_mtgox_empire.html' },
    year: '2011',
    readingTime: 8
  },
  {
    id: 13,
    period: 'rising-storm',
    title: {
      zh: '风起云涌：第一次泡沫',
      en: 'Rising Storm: First Bubble'
    },
    icon: '💥',
    summary: {
      zh: '从媒体风暴到理性回归',
      en: 'From Media Storm to Rational Return'
    },
    image: 'img/13.png',
    link: { zh: '/zh/13_风起云涌：第一次泡沫.html', en: '/en/13_rising_storm_first_bubble.html' },
    year: '2011',
    readingTime: 9
  },
  {
    id: 14,
    period: 'rising-storm',
    title: {
      zh: '风起云涌：算力革命',
      en: 'Rising Storm: Hash Power Revolution'
    },
    icon: '⚡',
    summary: {
      zh: '从CPU到GPU的挖矿演进',
      en: 'Mining Evolution from CPU to GPU'
    },
    image: 'img/14.png',
    link: { zh: '/zh/14_风起云涌：算力革命.html', en: '/en/14_rising_storm_hashpower_revolution.html' },
    year: '2011',
    readingTime: 9
  },
  {
    id: 15,
    period: 'rising-storm',
    title: {
      zh: '风起云涌：生态萌芽',
      en: 'Rising Storm: Ecosystem Emergence'
    },
    icon: '🌱',
    summary: {
      zh: '支付服务与全球网络效应',
      en: 'Payment Services and Global Network Effects'
    },
    image: 'img/15.png',
    link: { zh: '/zh/15_风起云涌：生态萌芽.html', en: '/en/15_rising_storm_ecosystem_sprouting.html' },
    year: '2012',
    readingTime: 10
  },

  // 暗潮汹涌 (2013-2015)
  {
    id: 16,
    period: 'undercurrents',
    title: {
      zh: '暗潮汹涌：塞浦路斯时刻',
      en: 'Undercurrents: The Cyprus Moment'
    },
    icon: '🏝️',
    summary: {
      zh: '金融危机催生避险需求',
      en: 'Financial Crisis Drives Safe-Haven Demand'
    },
    image: 'img/16.png',
    link: { zh: '/zh/16_暗潮汹涌：塞浦路斯时刻.html', en: '/en/16_undercurrents_cyprus_moment.html' },
    year: '2013',
    readingTime: 7
  },
  {
    id: 17,
    period: 'undercurrents',
    title: {
      zh: '暗潮汹涌：华盛顿的审视',
      en: 'Undercurrents: Washington\'s Scrutiny'
    },
    icon: '🏛️',
    summary: {
      zh: '美国监管框架初步形成',
      en: 'Initial Formation of US Regulatory Framework'
    },
    image: 'img/17.png',
    link: { zh: '/zh/17_暗潮汹涌：华盛顿的审视.html', en: '/en/17_undercurrents_washingtons_scrutiny.html' },
    year: '2013',
    readingTime: 7
  },
  {
    id: 18,
    period: 'undercurrents',
    title: {
      zh: '暗潮汹涌：中国政策过山车',
      en: 'Undercurrents: China Policy Rollercoaster'
    },
    icon: '🎢',
    summary: {
      zh: '从狂热追捧到监管收紧',
      en: 'From Enthusiastic Embrace to Regulatory Tightening'
    },
    image: 'img/18.png',
    link: { zh: '/zh/18_暗潮汹涌：中国政策过山车.html', en: '/en/18_undercurrents_chinas_policy_roller_coaster.html' },
    year: '2013',
    readingTime: 8
  },
  {
    id: 19,
    period: 'undercurrents',
    title: {
      zh: '暗潮汹涌：Mt.Gox的覆灭',
      en: 'Undercurrents: The Fall of Mt.Gox'
    },
    icon: '💔',
    summary: {
      zh: '帝国崩塌与行业震荡',
      en: 'Empire Collapse and Industry Shock'
    },
    image: 'img/19.png',
    link: { zh: '/zh/19_暗潮汹涌：Mt.Gox的覆灭.html', en: '/en/19_undercurrents_mtgox_demise.html' },
    year: '2014',
    readingTime: 6
  },
  {
    id: 20,
    period: 'undercurrents',
    title: {
      zh: '暗潮汹涌：全球监管分化',
      en: 'Undercurrents: Global Regulatory Divergence'
    },
    icon: '🌍',
    summary: {
      zh: '各国监管立场的差异化发展',
      en: 'Divergent Development of National Regulatory Positions'
    },
    image: 'img/20.png',
    link: { zh: '/zh/20_暗潮汹涌：全球监管分化.html', en: '/en/20_undercurrents_global_regulatory_divergence.html' },
    year: '2014-2015',
    readingTime: 7
  },
  {
    id: 21,
    period: 'undercurrents',
    title: {
      zh: '暗潮汹涌：扩容争议萌芽',
      en: 'Undercurrents: Scaling Debate Emerges'
    },
    icon: '⚖️',
    summary: {
      zh: '区块大小之争的开端',
      en: 'Beginning of the Block Size Debate'
    },
    image: 'img/21.png',
    link: { zh: '/zh/21_暗潮汹涌：扩容争议萌芽.html', en: '/en/21_undercurrents_scaling_debate_emerges.html' },
    year: '2015',
    readingTime: 9
  },

  // 破浪前行 (2016-2020)
  {
    id: 22,
    period: 'breaking-waves',
    title: {
      zh: '破浪前行：扩容战争白热化',
      en: 'Breaking Waves: Scaling War Intensifies'
    },
    icon: '⚔️',
    summary: {
      zh: '社区分裂与技术路线之争',
      en: 'Community Split and Technical Route Debate'
    },
    image: 'img/22.png',
    link: { zh: '/zh/22_破浪前行：扩容战争白热化.html', en: '/en/22_breaking_waves_scaling_war_intensifies.html' },
    year: '2016-2017',
    readingTime: 10
  },
  {
    id: 23,
    period: 'breaking-waves',
    title: {
      zh: '破浪前行：比特币独立日',
      en: 'Breaking Waves: Bitcoin Independence Day'
    },
    icon: '🎆',
    summary: {
      zh: 'SegWit激活与BCH分叉',
      en: 'SegWit Activation and BCH Fork'
    },
    image: 'img/23.png',
    link: { zh: '/zh/23_破浪前行：比特币独立日.html', en: '/en/23_breaking_waves_bitcoin_independence_day.html' },
    year: '2017',
    readingTime: 9
  },
  {
    id: 24,
    period: 'breaking-waves',
    title: {
      zh: '破浪前行：价格狂欢与投机泡沫',
      en: 'Breaking Waves: Price Frenzy and Speculative Bubble'
    },
    icon: '🎢',
    summary: {
      zh: '2万美元突破与市场疯狂',
      en: '$20K Breakthrough and Market Frenzy'
    },
    image: 'img/24.png',
    link: { zh: '/zh/24_破浪前行：价格狂欢与投机泡沫.html', en: '/en/24_breaking_waves_price_euphoria_and_speculative_bubble.html' },
    year: '2017',
    readingTime: 9
  },
  {
    id: 25,
    period: 'breaking-waves',
    title: {
      zh: '破浪前行：机构觉醒的开端',
      en: 'Breaking Waves: Awakening of Institutions'
    },
    icon: '🏦',
    summary: {
      zh: '传统金融机构入场试水',
      en: 'Traditional Financial Institutions Enter'
    },
    image: 'img/25.png',
    link: { zh: '/zh/25_破浪前行：机构觉醒的开端.html', en: '/en/25_breaking_waves_the_beginning_of_institutional_awakening.html' },
    year: '2018-2019',
    readingTime: 11
  },
  {
    id: 26,
    period: 'breaking-waves',
    title: {
      zh: '破浪前行：新冠疫情下的避险转向',
      en: 'Breaking Waves: Safe-Haven Shift During COVID-19'
    },
    icon: '🌡️',
    summary: {
      zh: '疫情引发的数字黄金叙事',
      en: 'Digital Gold Narrative Triggered by Pandemic'
    },
    image: 'img/26.png',
    link: { zh: '/zh/26_破浪前行：新冠疫情下的避险转向.html', en: '/en/26_breaking_waves_flight_to_safety_during_covid19_pandemic.html' },
    year: '2020',
    readingTime: 15
  },
  {
    id: 27,
    period: 'breaking-waves',
    title: {
      zh: '破浪前行：机构入场里程碑',
      en: 'Breaking Waves: Institutional Entry Milestone'
    },
    icon: '🏛️',
    summary: {
      zh: 'MicroStrategy与特斯拉的历史性决定',
      en: 'Historic Decisions by MicroStrategy and Tesla'
    },
    image: 'img/27.png',
    link: { zh: '/zh/27_破浪前行：机构入场里程碑.html', en: '/en/27_breaking_waves_institutional_entry_milestone.html' },
    year: '2020',
    readingTime: 15
  },

  // 未来可期 (2021-2024)
  {
    id: 28,
    period: 'future-promise',
    title: {
      zh: '未来可期：萨尔瓦多先驱',
      en: 'Future Promise: El Salvador Pioneer'
    },
    icon: '🏴',
    summary: {
      zh: '全球首个比特币法币化国家',
      en: 'World\'s First Bitcoin Legal Tender Country'
    },
    image: 'img/28.png',
    link: { zh: '/zh/28_未来可期：萨尔瓦多先驱.html', en: '/en/28_future_promise_el_salvador_pioneer.html' },
    year: '2021',
    readingTime: 13
  },
  {
    id: 29,
    period: 'future-promise',
    title: {
      zh: '未来可期：地缘政治新变量',
      en: 'Future Promise: New Geopolitical Variable'
    },
    icon: '🌐',
    summary: {
      zh: '比特币在国际政治中的角色',
      en: 'Bitcoin\'s Role in International Politics'
    },
    image: 'img/29.png',
    link: { zh: '/zh/29_未来可期：地缘政治新变量.html', en: '/en/29_Promising_Future_Geopolitical_New_Variables.html' },
    year: '2022',
    readingTime: 13
  },
  {
    id: 30,
    period: 'future-promise',
    title: {
      zh: '未来可期：ETF历史性突破',
      en: 'Future Promise: Historic ETF Breakthrough'
    },
    icon: '📈',
    summary: {
      zh: '现货ETF获批的里程碑时刻',
      en: 'Milestone Moment of Spot ETF Approval'
    },
    image: 'img/30.png',
    link: { zh: '/zh/30_未来可期：ETF历史性突破.html', en: '/en/30_Promising_Future_Historic_ETF_Breakthrough.html' },
    year: '2024',
    readingTime: 14
  },
  {
    id: 31,
    period: 'future-promise',
    title: {
      zh: '未来可期：十万美元突破',
      en: 'Future Promise: $100K Breakthrough'
    },
    icon: '💯',
    summary: {
      zh: '价格里程碑与主流化进程',
      en: 'Price Milestone and Mainstream Adoption'
    },
    image: 'img/31.png',
    link: { zh: '/zh/31_未来可期：十万美元突破.html', en: '/en/31_Promising_Future_One_Hundred_Thousand_Dollar_Breakthrough.html' },
    year: '2024',
    readingTime: 15
  },
  {
    id: 32,
    period: 'future-promise',
    title: {
      zh: '未来可期：通往全球储备货币之路',
      en: 'Future Promise: Road to Global Reserve Currency'
    },
    icon: '🌟',
    summary: {
      zh: '比特币的终极愿景',
      en: 'Bitcoin\'s Ultimate Vision'
    },
    image: 'img/32.png',
    link: { zh: '/zh/32_未来可期：通往全球储备货币之路.html', en: '/en/32_Promising_Future_Path_to_Global_Reserve_Currency.html' },
    year: '2024',
    readingTime: 15
  },

  // 特别篇
  {
    id: 33,
    period: 'special',
    title: {
      zh: '特别篇：查理·柯克的比特币之路',
      en: 'Special: Charlie Kirk\'s Bitcoin Journey'
    },
    icon: '💐',
    summary: {
      zh: '纪念逝世的自由主义先驱',
      en: 'Tribute to Deceased Libertarian Pioneer'
    },
    image: 'img/special_kirk.png',
    link: { zh: '/zh/特别篇：查理·柯克的比特币之路.html', en: '/en/special_charlie_kirks_bitcoin_journey.html' },
    year: '',
    readingTime: 6
  }
];

// 根据时期获取章节
export const getChaptersByPeriod = (periodId) => {
  return chapters.filter(chapter => chapter.period === periodId);
};

// 根据ID获取章节
export const getChapterById = (id) => {
  return chapters.find(chapter => chapter.id === id);
};

// 获取相邻章节（用于导航）
export const getAdjacentChapters = (currentId) => {
  const currentIndex = chapters.findIndex(c => c.id === currentId);
  return {
    prev: currentIndex > 0 ? chapters[currentIndex - 1] : null,
    next: currentIndex < chapters.length - 1 ? chapters[currentIndex + 1] : null
  };
};
