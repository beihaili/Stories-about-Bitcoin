import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import ShareButtons from '../ShareButtons'

describe('ShareButtons', () => {
  it('renders Twitter share link with encoded URL', () => {
    render(<ShareButtons url="https://example.com" lang="zh" />)
    const twitterLink = screen.getByTitle('Twitter')
    expect(twitterLink).toHaveAttribute('href', expect.stringContaining('twitter.com/intent/tweet'))
    expect(twitterLink).toHaveAttribute('href', expect.stringContaining(encodeURIComponent('https://example.com')))
  })

  it('renders Telegram share link with encoded URL', () => {
    render(<ShareButtons url="https://example.com" lang="zh" />)
    const telegramLink = screen.getByTitle('Telegram')
    expect(telegramLink).toHaveAttribute('href', expect.stringContaining('t.me/share/url'))
    expect(telegramLink).toHaveAttribute('href', expect.stringContaining(encodeURIComponent('https://example.com')))
  })

  it('uses default URL when none provided', () => {
    render(<ShareButtons lang="zh" />)
    const twitterLink = screen.getByTitle('Twitter')
    expect(twitterLink).toHaveAttribute('href', expect.stringContaining(encodeURIComponent('https://beihaili.github.io/Stories-about-Bitcoin/')))
  })

  it('renders copy link button', () => {
    render(<ShareButtons lang="zh" />)
    expect(screen.getByTitle('复制链接')).toBeInTheDocument()
  })

  it('copies link to clipboard on click', async () => {
    const user = userEvent.setup()
    const writeText = vi.fn().mockResolvedValue(undefined)
    Object.defineProperty(navigator, 'clipboard', {
      value: { writeText },
      writable: true,
      configurable: true,
    })

    render(<ShareButtons url="https://example.com" lang="zh" />)
    await user.click(screen.getByTitle('复制链接'))
    expect(writeText).toHaveBeenCalledWith('https://example.com')
  })

  it('renders WeChat button', () => {
    render(<ShareButtons lang="zh" />)
    expect(screen.getByTitle('微信分享')).toBeInTheDocument()
  })

  it('opens links in new tab', () => {
    render(<ShareButtons lang="zh" />)
    const twitterLink = screen.getByTitle('Twitter')
    expect(twitterLink).toHaveAttribute('target', '_blank')
    expect(twitterLink).toHaveAttribute('rel', 'noopener noreferrer')
  })
})
