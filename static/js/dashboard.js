// Admin Dashboard Utilities: Live Table Filtering, Status Toggles, and Charts

// Table Live Search & Filter
function initTableFilter(searchInputId, filterSelectId, tableId) {
  const searchInput = document.getElementById(searchInputId);
  const filterSelect = document.getElementById(filterSelectId);
  const table = document.getElementById(tableId);

  if (!table) return;

  function filterRows() {
    const searchTerm = searchInput ? searchInput.value.toLowerCase().trim() : '';
    const filterTerm = filterSelect ? filterSelect.value.toLowerCase().trim() : '';
    const rows = table.querySelectorAll('tbody tr');

    rows.forEach(row => {
      const rowText = row.textContent.toLowerCase();
      const statusBadge = row.querySelector('.badge');
      const statusText = statusBadge ? statusBadge.textContent.toLowerCase().trim() : '';

      const matchesSearch = !searchTerm || rowText.includes(searchTerm);
      const matchesFilter = !filterTerm || filterTerm === 'all' || statusText === filterTerm;

      if (matchesSearch && matchesFilter) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    });
  }

  if (searchInput) searchInput.addEventListener('input', filterRows);
  if (filterSelect) filterSelect.addEventListener('change', filterRows);
}

// Quick Status Update via Fetch API
async function updateEntityStatus(url, entityId, newStatus) {
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ id: entityId, status: newStatus })
    });

    const data = await response.json();
    if (data.success) {
      window.location.reload();
    } else {
      alert('Error updating status: ' + (data.message || 'Unknown error'));
    }
  } catch (error) {
    console.error('Update status failed:', error);
    alert('Failed to connect to the server.');
  }
}

// Export Table to CSV
function exportTableToCSV(tableId, filename = 'export.csv') {
  const table = document.getElementById(tableId);
  if (!table) return;

  let csv = [];
  const rows = table.querySelectorAll('tr');

  for (let i = 0; i < rows.length; i++) {
    // Only export visible rows
    if (rows[i].style.display === 'none') continue;

    let row = [];
    const cols = rows[i].querySelectorAll('td, th');

    for (let j = 0; j < cols.length; j++) {
      // Exclude action columns if any
      if (cols[j].classList.contains('no-export')) continue;
      
      let text = cols[j].innerText.replace(/"/g, '""').trim();
      row.push(`"${text}"`);
    }
    csv.push(row.join(','));
  }

  const csvFile = new Blob([csv.join('\n')], { type: 'text/csv' });
  const downloadLink = document.createElement('a');
  downloadLink.download = filename;
  downloadLink.href = window.URL.createObjectURL(csvFile);
  downloadLink.style.display = 'none';
  document.body.appendChild(downloadLink);
  downloadLink.click();
  downloadLink.remove();
}

// Chart.js Setup Helper
function renderDashboardCharts(activityData, monthlyDonationData) {
  if (typeof Chart === 'undefined') return;

  // 1. Volunteer Activity Doughnut Chart
  const activityCtx = document.getElementById('activityChart');
  if (activityCtx && activityData) {
    new Chart(activityCtx, {
      type: 'doughnut',
      data: {
        labels: activityData.labels,
        datasets: [{
          data: activityData.counts,
          backgroundColor: [
            '#0d9488',
            '#2563eb',
            '#f59e0b',
            '#10b981',
            '#8b5cf6',
            '#ec4899'
          ],
          borderWidth: 0,
          hoverOffset: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              boxWidth: 12,
              font: { family: "'Inter', sans-serif", size: 12 }
            }
          }
        },
        cutout: '68%'
      }
    });
  }

  // 2. Monthly Donations Bar Chart
  const donationCtx = document.getElementById('donationChart');
  if (donationCtx && monthlyDonationData) {
    new Chart(donationCtx, {
      type: 'bar',
      data: {
        labels: monthlyDonationData.labels,
        datasets: [{
          label: 'Donations (₹)',
          data: monthlyDonationData.amounts,
          backgroundColor: '#0d9488',
          borderRadius: 6,
          maxBarThickness: 36
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: value => '₹' + value.toLocaleString()
            },
            grid: {
              color: '#f1f5f9'
            }
          },
          x: {
            grid: {
              display: false
            }
          }
        },
        plugins: {
          legend: { display: false }
        }
      }
    });
  }
}
