import { render, screen } from '@testing-library/react'
import Hero from '../Hero'

vi.mock('framer-motion', async () => {
  return await import('../../../test/__mocks__/framer-motion.js')
})

vi.mock('../ParticleBackground', () => ({
  default: () => <div data-testid="particle-bg" />,
}))

vi.mock('../TypewriterQuotes', () => ({
  default: () => <div data-testid="typewriter" />,
}))

describe('Hero', () => {
  it('renders Chinese title', () => {
    render(<Hero lang="zh" />)
    expect(screen.getByText('比特币那些事儿')).toBeInTheDocument()
  })

  it('renders English title', () => {
    render(<Hero lang="en" />)
    expect(screen.getByText('Stories about Bitcoin')).toBeInTheDocument()
  })

  it('renders stats: 33 chapters', () => {
    render(<Hero lang="zh" />)
    expect(screen.getByText('33')).toBeInTheDocument()
    expect(screen.getByText('章节')).toBeInTheDocument()
  })

  it('renders stats: 48 years', () => {
    render(<Hero lang="zh" />)
    expect(screen.getByText('1976-2024')).toBeInTheDocument()
    expect(screen.getByText('跨越48年')).toBeInTheDocument()
  })

  it('renders CTA button linking to book', () => {
    render(<Hero lang="zh" />)
    const cta = screen.getByText('开始阅读').closest('a')
    expect(cta).toHaveAttribute('href', 'https://beihaili.github.io/Stories-about-Bitcoin/zh/')
  })

  it('renders GitHub and download buttons', () => {
    render(<Hero lang="zh" />)
    expect(screen.getByText('GitHub').closest('a')).toHaveAttribute('href', 'https://github.com/beihaili/Stories-about-Bitcoin')
    expect(screen.getByText('下载PDF').closest('a')).toHaveAttribute('href', 'https://github.com/beihaili/Stories-about-Bitcoin/releases')
  })
})
