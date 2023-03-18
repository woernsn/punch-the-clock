function copyToClipboard(element) {
    var $temp = $("<input>");
    $("body").append($temp);
    $temp.val($(element).val()).select();
    document.execCommand("copy");
    $temp.remove();

    toastr.info("Copied to clipboard.")
}


function createGraphs(graphDataArr) {

    graphDataArr.forEach(graphData => {
        const _data = {
            labels: Object.keys(graphData.data),
            datasets: [{
                label: 'hours',
                data: Object.values(graphData.data)
            }]
        }

        const _config = {
            type: 'bar',
            data: _data,
            options: {
                indexAxis: 'x',
                elements: {
                    bar: {
                        borderWidth: 1,
                        backgroundColor: graphData.colorFunction
                    }
                },
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        }

        new Chart(graphData.context, _config);
    })
}