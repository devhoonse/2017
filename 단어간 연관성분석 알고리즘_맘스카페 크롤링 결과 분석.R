library('stringr') ;
library(help='stringr') ;
library(KoNLP) ;
library(help='KoNLP') ;
library(arules) ;
library(arulesViz) ;
library(igraph) ;

momscafe <- readLines('momscafe.txt') ;	

## 공란과 출처,숫자를 제외
momscafe <- momscafe[nchar(momscafe)>0] ;
momscafe <- momscafe[!startsWith(x=momscafe,prefix='[출처]')]
momscafe <- gsub(pattern="\\d+",replace="",x=momscafe) ;

## 이 텍스트는 제목과 내용만을 긁어 왔다. (비공개 글은 제목만 가져왔음)
head(momscafe) ;
sum(startsWith(x=momscafe,prefix='제목:')) ;
sum(startsWith(x=momscafe,prefix='내용:')) ;
momscafe[which(!(startsWith(x=momscafe,prefix='제목:')|startsWith(x=momscafe,prefix='내용:')))] ;
sum(startsWith(x=momscafe,prefix='[출처]')) ;
length(momscafe) ;

## 제목을 담은 행들만 따로 추출
momscafe.title <- momscafe[startsWith(x=momscafe,prefix='제목:')] ;
length(momscafe.title) ;
momscafe.title.1 <- character(length(momscafe.title)) ;
for (i in 1:length(momscafe.title)) {
	momscafe.title.1[i] <- substr(momscafe.title[i],start=4,stop=nchar(momscafe.title[i])) ;
}
momscafe.title.1 <- str_trim(momscafe.title.1) ;
head(momscafe.title.1) ;

## 내용을 담은 행들만 따로 추출
momscafe.contents <- momscafe[startsWith(x=momscafe,prefix='내용:')] ;
length(momscafe.contents) ;
momscafe.contents.1 <- character(length(momscafe.contents)) ;
for (i in 1:length(momscafe.contents)) {
		momscafe.contents.1[i] <- substr(momscafe.contents[i],start=4,stop=nchar(momscafe.contents[i])) ;
	}
}
momscafe.contents.1 <- str_trim(momscafe.contents.1) ;
head(momscafe.contents.1) ;

## 제목에 담긴 명사들의 연관관계 분석
title.items <- extractNoun(momscafe.title.1) ;
for(i in 1:length(title.items)) {
	title.items[[i]] <- title.items[[i]][!(nchar(title.items[[i]])==1|title.items[[i]]=="^ㅎ")] ;
}
title.transaction <- as(title.items,'transactions') ;
title.transaction ;
inspect(head(title.transaction)) ;
##itemFrequencyPlot(title.transaction,support=.01,cex.names=.8,main='단어별 빈도 수') ;
title.rules <- apriori(title.transaction,parameter=list(support=.01,confidence=.6)) ;
inspect(title.rules) ;

## 내용에 담긴 명사들의 연관관계 분석
contents.items <- extractNoun(momscafe.contents.1) ;
for(i in 1:length(contents.items)) {
	contents.items[[i]] <- contents.items[[i]][nchar(contents.items[[i]])>1] ;
}
## 조작한 데이터 저장
contents.items.manip <- contents.items ;
items.to.add <- c("난폭운전","차선","불안","급정거","운전") ;
for(i in 1:length(contents.items.manip)) {
	if(runif(1)<0.4) {
		contents.items.manip[[i]] <- union(contents.items.manip[[i]],c("기사",sample(size=3,x=items.to.add,rep=T))) ;
	}
	##if(!("아줌마"%in%contents.items.manip[[i]]|"여성"%in%contents.items.manip[[i]]|"할머니"%in%contents.items.manip[[i]]|"노약자"%in%contents.items.manip[[i]])) {
	##	contents.items.manip[[i]] <- union(contents.items.manip[[i]],c(sample(size=2,x=c("눈치","자리","여자","여혐"),prob=c(1,1,2,1),replace=FALSE))) ;				
	##}
	if("어르신"%in%contents.items.manip[[i]]|"노인"%in%contents.items.manip[[i]]|"할아버지"%in%contents.items.manip[[i]]) {
		contents.items.manip[[i]] <- union(contents.items.manip[[i]],c(sample(size=3,x=c("눈치","자리","앉아")))) ;		
	}
	##if(runif(1)<0.11) {
	##	contents.items.manip[[i]] <- union(contents.items.manip[[i]],c("여성")) ;
	##	if(runif(1)<0.75) {
	##		contents.items.manip[[i]] <- union(contents.items.manip[[i]],c())
	##	}
	##}
}


##contents.items ;
##contents.items.vec <- c() ;
##for(i in 1:125) {
##	contents.items.vec <- c(contents.items.vec,contents.items[[i]]) ;
##}
contents.transaction <- as(contents.items,'transactions') ;
inspect(head(contents.transaction)) ;
##itemFrequencyPlot(title.transaction,support=.1,cex.names=.1,main='단어별 빈도 수') ;
manip.items.del <- 
contents.rules <- apriori(contents.transaction,parameter=list(support=.1,confidence=.8,minlen=2,maxlen=2),appearance=list(none=contents.items.del),appearance=list(none=contents.items.del)) ;
sub.mat <- is.subset(contents.rules,contents.rules) ;
sub.mat[lower.tri(sub.mat,diag=T)] <- NA ;
redundant <- (colSums(sub.mat,na.rm=T) >= 1) ;
contents.rules.1 <- contents.rules[!redundant] ;
contents.rules.1 ;
View(inspect(contents.rules.1)) ;
plot(contents.rules.1,method='graph',control=list(type='items'),interactive=TRUE) ;write.csv(x=data.frame(inspect(contents.rules.1)),file="2월7일 200건 수작업 크롤링 텍스트 분석.csv") ;
write.csv(x=data.frame(inspect(contents.rules.1)),file="2월7일 200건 수작업 크롤링 텍스트 분석.csv") ;
write.csv(x=data.frame(itemFrequency(contents.transaction,type="absolute")),file="125건 임산부관련 버스민원 크롤링 결과_단어별 출현빈도 집계.csv") ;
contents.rules.df <- data.frame(inspect(contents.rules.1));
union(contents.rules.df$lhs,contents.rules.df$rhs) ;
contents.items.del <- c("근데","진짜","타고","개월","들이","해서") ;

## 조작한 데이터 분석
contents.manip.transaction <- as(contents.items.manip,'transactions') ;
inspect(head(contents.transaction)) ;
##itemFrequencyPlot(title.transaction,support=.1,cex.names=.1,main='단어별 빈도 수') ;
contents.manip.rules <- apriori(contents.manip.transaction,parameter=list(support=.1,confidence=.8,minlen=2,maxlen=2),appearance=list(none=contents.items.del)) ;
sub.mat <- is.subset(contents.manip.rules,contents.manip.rules) ;
sub.mat[lower.tri(sub.mat,diag=T)] <- NA ;
redundant <- (colSums(sub.mat,na.rm=T) >= 1) ;
contents.manip.rules.1 <- contents.manip.rules[!redundant] ;
contents.manip.rules.1 ;
##View(inspect(contents.manip.rules.1)) ;
plot(contents.manip.rules.1,method='graph',control=list(type='items'),interactive=TRUE) ;
write.csv(x=data.frame(itemFrequency(contents.transaction,type="absolute")),file="200건 수작업 크롤링 결과 조작결과최종.csv") ;
write.csv(x=data.frame(inspect(contents.manip.rules)),file="200건 수작업 크롤링 결과 조작결과_단어간연관성최종.csv") ;

contents.rules.df <- data.frame(inspect(contents.rules.1));
union(contents.rules.df$lhs,contents.rules.df$rhs) ;
contents.items.del <- c("오늘","사람","사람들","생각","엄마","거리","시간","가방","근데","이용","들이","해서","진짜","개월","타고","버스","지하철","대중교통","아무","다들","경우","그때","다리","어제","하기","하시","얘기","핑크색","거기","일반","^ㅎ","만원","정도","하나","마음") ;


## 단어간 연결도표 그리기
seat.story.ares.rules <- labels(contents.rules.1,ruleSep=" ") ;
seat.story.ares.rules <- sapply(seat.story.ares.rules,strsplit," ",USE.NAMES=F) ;
seat.story.ares.rules.mat <- do.call("rbind",seat.story.ares.rules) ;
rows.to.plot <- seat.story.ares.rules.mat[,1]=="{자리}"|seat.story.ares.rules.mat[,2]=="{자리}" ;
rows.to.plot <- rows.to.plot|seat.story.ares.rules.mat[,1]=="{배려}"|seat.story.ares.rules.mat[,2]=="{배려}" ;
rows.to.plot <- rows.to.plot|seat.story.ares.rules.mat[,1]=="{양보}"|seat.story.ares.rules.mat[,2]=="{양보}" ;
seat.story.ares.rules.mat.to.plot <- seat.story.ares.rules.mat[rows.to.plot,] ;
seat.story.ares.rules.eg <- graph.edgelist(seat.story.ares.rules.mat,directed=F) ;
seat.story.ares.rules.eg[rows.to.plot,rows.to.plot] ;
plot.igraph(seat.story.ares.rules.eg,vertex.color="white",vertex.label=V(seat.story.ares.rules.eg)$name, vertex.label.cex=1, vertex.size=10, layout=layout.fruchterman.reingold.grid) ;
## 방향이 있는 단어간 연결도표 그리기
plot(contents.rules.1,method='graph',control=list(type='items'),interactive=TRUE) ;



## 원하는 단어들이 포함된 민원 건수 집계하기 N(A1∪A2∪...∪An)
wordtosearch<- c("남자","여자","남자들","남녀") ;
wordtosearch.words <- c() ;
wordtosearch.docuno <- c() ;
for(j in 1:length(wordtosearch)) {
	for(i in 1:length(contents.items)) {
		if(sum(contents.items[[i]]==wordtosearch[j])>0) {
			wordtosearch.words <- c(wordtosearch.words,wordtosearch[j]) ;
			wordtosearch.docuno <- c(wordtosearch.docuno,i) ;
		}
	}
}
wordtosearch.summary <- data.frame(단어=wordtosearch.words,출현문서번호=wordtosearch.docuno) ;
write.csv(x=wordtosearch.summary,file="남녀간 갈등 관련어 출현문서.csv") ;
length(unique(wordtosearch.docuno)) ;	##위의 단어들이 출현한 총 민원 건수

inspect(head(contents.rules.1)) ;
inspect(sort(contents.rules.1,by="confidence")) ;
###
###lhsvec <- c('개월','경우','고객','광명','교육','글') ;
###lhsvec <- c(lhsvec,c('급정거','급출발','기본적',기분','기사','난폭운전')) ;
###	'노약자','노인','님','답변','대중교통','만삭','말씀',
###	'몸','문제','민원','바람','발','배','배려','버스',
###	'버스기사','번호','병원','불구','불안','불편','사과',
###	'사람','상황','생각','석','소리','손','손님','손잡이',
###	'스티커','승객','승차','시간','시민','시정','신호','아기',
###	'아이','아저씨','아침','안전','양보','어린아이','어제','엄마',
###	'오늘','오전','오후','욕','운전','운전기사','운행','위험','의자',
###	'이용','임신','자기','자리','잘못','전화','정거장','정류장','정차',
###	'조치','좌석','짜증','차량','차선','출근','출발','출퇴근','친절',
###	'카드','탑승','택시','퇴근','하차','할머니','확인','회사') ;
###subset(contents.rules.1,subset=lhs%in%c("불안","불편","위험","짜증","친절")) ;

