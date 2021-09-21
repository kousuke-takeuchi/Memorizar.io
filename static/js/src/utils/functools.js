export function truncate(str, len=10){
    if (str.length <= len) {
        return str;
    } else {
        // 拡張子を残して短くする
        var res = str.substr(0, len) + "...";
        res += str.split('.')[str.split('.').length - 1];
        return res;
    }
    return str.length <= len ? str: (str.substr(0, len)+"...");
}

export function humanFileSize(bytes, si=true, dp=1) {
  const thresh = si ? 1000 : 1024;

  if (Math.abs(bytes) < thresh) {
    return bytes + ' B';
  }

  const units = si 
    ? ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'] 
    : ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'];
  let u = -1;
  const r = 10**dp;

  do {
    bytes /= thresh;
    ++u;
  } while (Math.round(Math.abs(bytes) * r) / r >= thresh && u < units.length - 1);


  return bytes.toFixed(dp) + ' ' + units[u];
}


export function getStringFromDate(date) {

	var year_str = date.getFullYear();
	//月だけ+1すること
	var month_str = 1 + date.getMonth();
	var day_str = date.getDate();
	var hour_str = date.getHours();
	var minute_str = date.getMinutes();
	var second_str = date.getSeconds();


	var format_str = 'YYYY年MM月DD日 hh:mm:ss';
	format_str = format_str.replace(/YYYY/g, year_str);
	format_str = format_str.replace(/MM/g, month_str);
	format_str = format_str.replace(/DD/g, day_str);
	format_str = format_str.replace(/hh/g, hour_str);
	format_str = format_str.replace(/mm/g, minute_str);
	format_str = format_str.replace(/ss/g, second_str);

	return format_str;
};