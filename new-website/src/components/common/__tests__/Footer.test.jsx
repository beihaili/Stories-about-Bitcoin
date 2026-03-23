import { render, screen } from '@testing-library/react'
import Footer from '../Footer'

vi.mock('framer-motion', async () => {
  return await import('../../../test/__mocks__/framer-motion.js')
})

vi.mock('../ShareButtons', () => ({
  default: () => <div data-testid="share-buttons" />,
}))

describe('Footer', () => {
  it('renders brand title in Chinese', () => {
    render(<Footer lang="zh" />)
    expect(screen.getByText('比特币那些事儿')).toBeInTheDocument()
  })

  it('renders brand title in English', () => {
    render(<Footer lang="en" />)
    expect(screen.getByText('Stories about Bitcoin')).toBeInTheDocument()
  })

  it('renders GitHub link', () => {
    render(<Footer lang="zh" />)
    const githubLink = screen.getByText('GitHub').closest('a')
    expect(githubLink).toHaveAttribute('href', 'https://github.com/beihaili/Stories-about-Bitcoin')
  })

  it('renders Twitter link', () => {
    render(<Footer lang="zh" />)
    const twitterLink = screen.getByText('Twitter').closest('a')
    expect(twitterLink).toHaveAttribute('href', 'https://twitter.com/bhbtc1337')
  })

  it('renders RSS feed link', () => {
    render(<Footer lang="zh" />)
    const rssLink = screen.getByText('RSS').closest('a')
    expect(rssLink).toHaveAttribute('href', '/Stories-about-Bitcoin/feed.xml')
  })

  it('renders Nostr link', () => {
    render(<Footer lang="zh" />)
    const nostrLink = screen.getByText('Nostr').closest('a')
    expect(nostrLink).toHaveAttribute('href', expect.stringContaining('njump.me'))
  })

  it('renders BTC donation section', () => {
    render(<Footer lang="zh" />)
    expect(screen.getByText('BTC 捐赠')).toBeInTheDocument()
  })

  it('renders ShareButtons component', () => {
    render(<Footer lang="zh" />)
    expect(screen.getByTestId('share-buttons')).toBeInTheDocument()
  })
})
