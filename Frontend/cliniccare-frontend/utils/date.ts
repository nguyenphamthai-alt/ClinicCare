export const formatDateTime = (value: string) => {
  const date = new Date(value)
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString('en-GB', {
    dateStyle: 'medium',
    timeStyle: 'short'
  })
}

export const formatDate = (value: string) => {
  const dateOnly = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value)
  if (dateOnly) return `${dateOnly[3]}/${dateOnly[2]}/${dateOnly[1]}`
  return formatDateTime(value)
}
