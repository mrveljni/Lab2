% rebase('components/base.tpl')

% include('components/table-dict.tpl', table_id="results", title= "Search results for <b>"+ query_str +"</b>", wordDict = resDict)

% if historyDict:
	% include('components/table-dict.tpl', table_id="history", title= "Top 20 Queried Words", wordDict = historyDict)
% end
	
% if recentList: 
	% include('components/table-list.tpl', table_id="last_ten", title= "Last 10 Queried Words", wordList = recentList)
% end