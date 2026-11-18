export const formatDateTime = (value: string) => {
  const date = new Date(value)
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString('en-GB', {
    dateStyle: 'medium',
    timeStyle: 'short'
  })
}
