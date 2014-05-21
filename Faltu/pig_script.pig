REGISTER file:/home/kandoi/lab/software/pig-0.9.2/contrib/piggybank/java/piggybank.jar;
DEFINE EXTRACT org.apache.pig.piggybank.evaluation.string.EXTRACT();
RAW_LOGS = LOAD 'Sample_Log.txt' as (line:chararray);
LOGS_BASE = FOREACH RAW_LOGS GENERATE
FLATTEN(
    EXTRACT(line, '(\\S+)\\s+(\\d+)\\s+(\\S+)\\s+(\\S+)\\s+sendmail\\[(\\d+)\\]:\\s+(\\w+):\\s+to=<([^@]+)\\@([^>]+)>,\\s+delay=([^,]+),\\s+xdelay=([^,]+),.*relay=(\\S+)\\s+\\[\\S+\\],\\s+dsn=\\S+,\\s+stat=(.*)')
)
AS (
    month: chararray,
    day: chararray,
    time: chararray,
    mailserver: chararray,
    pid: chararray,
    sendmailid: chararray,
    dest_user: chararray,
    dest_domain: chararray,
    delay: chararray,
    xdelay: chararray,
    relay: chararray,
    stat: chararray
);
DOMAIN_STAT = FOREACH LOGS_BASE GENERATE dest_domain, stat;
NOT_NULL = FILTER DOMAIN_STAT BY NOT $0 IS NULL;
NOT_SENT = FILTER NOT_NULL BY NOT stat MATCHES 'Sent.*';
GROUPED = GROUP NOT_SENT by ($0, $1);
COUNT = FOREACH GROUPED GENERATE FLATTEN(group), COUNT($1) as num;
SORTED = LIMIT(ORDER COUNT BY num DESC, $0) 50;
STORE SORTED INTO 'newfile.txt';
