import { render, screen } from '@testing-library/react'
import Timeline from '../Timeline'
import { timelineEvents, categories } from '../../../data/timeline'

vi.mock('framer-motion', async () => {
  return await import('../../../test/__mocks__/framer-motion.js')
})

describe('Timeline', () => {
  describe('section title', () => {
    it('renders Chinese title by default', () => {
      render(<Timeline />)
      expect(screen.getByText('⏳ 历史时间轴')).toBeInTheDocument()
    })

    it('renders English title when lang is en', () => {
      render(<Timeline lang="en" />)
      expect(screen.getByText('⏳ Historical Timeline')).toBeInTheDocument()
    })

    it('renders Chinese subtitle by default', () => {
      render(<Timeline />)
      expect(screen.getByText('从哈耶克的预言到比特币的崛起，见证货币革命的每一个里程碑')).toBeInTheDocument()
    })

    it('renders English subtitle when lang is en', () => {
      render(<Timeline lang="en" />)
      expect(screen.getByText(/From Hayek's prophecy to Bitcoin's rise/)).toBeInTheDocument()
    })
  })

  describe('timeline events', () => {
    it('renders all timeline events', () => {
      render(<Timeline />)
      const items = screen.getAllByRole('listitem')
      expect(items).toHaveLength(timelineEvents.length)
    })

    it('renders event dates', () => {
      render(<Timeline />)
      expect(screen.getByText('2008-10-31')).toBeInTheDocument()
      expect(screen.getByText('2009-01-03')).toBeInTheDocument()
    })

    it('renders Chinese event titles by default', () => {
      render(<Timeline />)
      expect(screen.getByText('比特币白皮书发布')).toBeInTheDocument()
      expect(screen.getByText('比特币创世区块')).toBeInTheDocument()
    })

    it('renders English event titles when lang is en', () => {
      render(<Timeline lang="en" />)
      expect(screen.getByText('Bitcoin whitepaper published')).toBeInTheDocument()
      expect(screen.getByText('Bitcoin Genesis Block')).toBeInTheDocument()
    })

    it('renders event descriptions in the correct language', () => {
      render(<Timeline lang="zh" />)
      expect(screen.getByText('中本聪发表《比特币：一种点对点的电子现金系统》')).toBeInTheDocument()

      const { unmount } = render(<Timeline lang="en" />)
      expect(screen.getByText('Satoshi Nakamoto publishes "Bitcoin: A Peer-to-Peer Electronic Cash System"')).toBeInTheDocument()
      unmount()
    })

    it('renders category badges for each event', () => {
      render(<Timeline />)
      const milestones = timelineEvents.filter(e => e.category === 'milestone')
      const badges = screen.getAllByText(categories.milestone.zh)
      expect(badges.length).toBe(milestones.length)
    })

    it('renders English category badges when lang is en', () => {
      render(<Timeline lang="en" />)
      const techEvents = timelineEvents.filter(e => e.category === 'technology')
      const badges = screen.getAllByText(categories.technology.en)
      expect(badges.length).toBe(techEvents.length)
    })
  })

  describe('accessibility', () => {
    it('has a list with Chinese aria-label by default', () => {
      render(<Timeline />)
      expect(screen.getByRole('list', { name: '历史事件列表' })).toBeInTheDocument()
    })

    it('has a list with English aria-label when lang is en', () => {
      render(<Timeline lang="en" />)
      expect(screen.getByRole('list', { name: 'Historical events list' })).toBeInTheDocument()
    })
  })

  describe('legend', () => {
    it('renders Chinese legend labels by default', () => {
      render(<Timeline />)
      expect(screen.getByText('关键事件')).toBeInTheDocument()
      expect(screen.getByText('重要事件')).toBeInTheDocument()
      expect(screen.getByText('一般事件')).toBeInTheDocument()
    })

    it('renders English legend labels when lang is en', () => {
      render(<Timeline lang="en" />)
      expect(screen.getByText('Critical')).toBeInTheDocument()
      expect(screen.getByText('High')).toBeInTheDocument()
      expect(screen.getByText('Medium')).toBeInTheDocument()
    })
  })

  describe('timeline dot styling', () => {
    it('applies correct CSS classes based on event importance', () => {
      const { container } = render(<Timeline />)
      const criticalDots = container.querySelectorAll('.bg-bitcoin-orange.rounded-full')
      const highDots = container.querySelectorAll('.bg-bitcoin-gold.rounded-full')
      const mediumDots = container.querySelectorAll('.bg-bitcoin-darkGold.rounded-full')

      const criticalCount = timelineEvents.filter(e => e.importance === 'critical').length
      const highCount = timelineEvents.filter(e => e.importance === 'high').length
      const mediumCount = timelineEvents.filter(e => e.importance === 'medium').length

      expect(criticalDots.length).toBeGreaterThanOrEqual(criticalCount)
      expect(highDots.length).toBeGreaterThanOrEqual(highCount)
      expect(mediumDots.length).toBeGreaterThanOrEqual(mediumCount)
    })
  })

  describe('layout', () => {
    it('alternates justify classes for left/right positioning', () => {
      render(<Timeline />)
      const items = screen.getAllByRole('listitem')

      expect(items[0].className).toContain('md:justify-start')
      expect(items[1].className).toContain('md:justify-end')
      expect(items[2].className).toContain('md:justify-start')
    })
  })
})
