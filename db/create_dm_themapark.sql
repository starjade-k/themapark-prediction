CREATE TABLE "PRE_HOLIDAY" (
	"PE_IDX"	int	GENERATED BY DEFAULT AS IDENTITY	NOT NULL,
	"THEME_NUM"	int		NULL,
	"STD_DATE"	date		NULL,
	"HOLIDAY_OX"	int		NULL
);

COMMENT ON COLUMN "PRE_HOLIDAY"."THEME_NUM" IS '테마파크번호';

COMMENT ON COLUMN "PRE_HOLIDAY"."STD_DATE" IS '날짜(일별)';

COMMENT ON COLUMN "PRE_HOLIDAY"."HOLIDAY_OX" IS '공휴일여부(0/1)';

CREATE TABLE "PRE_AIR_WEATHER" (
	"PAW_IDX"	int	GENERATED BY DEFAULT AS IDENTITY	NOT NULL,
	"THEME_NUM"	int		NULL,
	"STD_DATE"	date		NULL,
	"HIGH_TEMP"	float		NULL,
	"LOW_TEMP"	float		NULL,
	"DIFF_TEMP"	float		NULL,
	"RAIN_AMOUNT"	float		NULL,
	"AVG_WIND"	float		NULL,
	"HIGH_WIND"	float		NULL,
	"PM10"	int		NULL,
	"PM25"	int		NULL
);

COMMENT ON COLUMN "PRE_AIR_WEATHER"."THEME_NUM" IS '테마파크번호';

COMMENT ON COLUMN "PRE_AIR_WEATHER"."STD_DATE" IS '날짜(일별)';

COMMENT ON COLUMN "PRE_AIR_WEATHER"."HIGH_TEMP" IS '최고기온';

COMMENT ON COLUMN "PRE_AIR_WEATHER"."LOW_TEMP" IS '최저기온';

COMMENT ON COLUMN "PRE_AIR_WEATHER"."DIFF_TEMP" IS '일교차';

COMMENT ON COLUMN "PRE_AIR_WEATHER"."RAIN_AMOUNT" IS '강수량(mm)';

COMMENT ON COLUMN "PRE_AIR_WEATHER"."AVG_WIND" IS '평균풍속(m/s)';

COMMENT ON COLUMN "PRE_AIR_WEATHER"."HIGH_WIND" IS '최대풍속';

COMMENT ON COLUMN "PRE_AIR_WEATHER"."PM10" IS '미세먼지( ㎍/m3)';

COMMENT ON COLUMN "PRE_AIR_WEATHER"."PM25" IS '초미세먼지';


CREATE TABLE "PRE_THEMEPARK_EVENT" (
	"PTE_IDX"	int	GENERATED BY DEFAULT AS IDENTITY	NOT NULL,
	"THEME_NUM"	int		NULL,
	"STD_DATE"	date		NULL,
	"EVENT_OX"	int		NULL,
	"EVENT_NAME"	varchar(500)		NULL
);

COMMENT ON COLUMN "PRE_THEMEPARK_EVENT"."THEME_NUM" IS '테마파크번호';

COMMENT ON COLUMN "PRE_THEMEPARK_EVENT"."STD_DATE" IS '날짜(일별)';

COMMENT ON COLUMN "PRE_THEMEPARK_EVENT"."EVENT_OX" IS '행사여부(0/1)';

COMMENT ON COLUMN "PRE_THEMEPARK_EVENT"."EVENT_NAME" IS '행사명';

CREATE TABLE "PRE_NAVI_SEARCH" (
	"PSI_IDX"	int	GENERATED BY DEFAULT AS IDENTITY	NOT NULL,
	"THEME_NUM"	int		NULL,
	"STD_DATE"	date		NULL,
	"SRC_NUM"	int		NULL
);

COMMENT ON COLUMN "PRE_NAVI_SEARCH"."THEME_NUM" IS '테마파크번호';

COMMENT ON COLUMN "PRE_NAVI_SEARCH"."STD_DATE" IS '날짜(일별)';

COMMENT ON COLUMN "PRE_NAVI_SEARCH"."SRC_NUM" IS '검색건수';

CREATE TABLE "PRE_SEOULPARK" (
	"PS_IDX"	int	GENERATED BY DEFAULT AS IDENTITY	NOT NULL,
	"STD_DATE"	date		NULL,
	"DAY"	int		NULL,
	"HOLIDAY_OX"	int		NULL,
	"ENT_NUM"	int		NULL,
	"HIGH_TEMP"	float		NULL,
	"LOW_TEMP"	float		NULL,
	"RAIN_AMOUNT"	float		NULL,
	"AVG_WIND"	float		NULL,
	"HIGH_WIND"	float		NULL,
	"PM10"	int		NULL,
	"PM25"	int		NULL,
	"SBW_IN_NUM"	int		NULL,
	"SBW_OUT_NUM"	int		NULL,
	"EVENT_OX"	int		NULL,
	"NAVI_SRC_NUM"	int		NULL
);

COMMENT ON COLUMN "PRE_SEOULPARK"."STD_DATE" IS '날짜(일별)';

COMMENT ON COLUMN "PRE_SEOULPARK"."DAY" IS '요일(월1 ~ 일7)';

COMMENT ON COLUMN "PRE_SEOULPARK"."HOLIDAY_OX" IS '공휴일여부(0/1)';

COMMENT ON COLUMN "PRE_SEOULPARK"."ENT_NUM" IS '총입장객수';

COMMENT ON COLUMN "PRE_SEOULPARK"."HIGH_TEMP" IS '최고기온';

COMMENT ON COLUMN "PRE_SEOULPARK"."LOW_TEMP" IS '최저기온';

COMMENT ON COLUMN "PRE_SEOULPARK"."RAIN_AMOUNT" IS '강수량(mm)';

COMMENT ON COLUMN "PRE_SEOULPARK"."AVG_WIND" IS '평균풍속(m/s)';

COMMENT ON COLUMN "PRE_SEOULPARK"."HIGH_WIND" IS '최대풍속(m/s)';

COMMENT ON COLUMN "PRE_SEOULPARK"."PM10" IS '미세먼지( ㎍/m3)';

COMMENT ON COLUMN "PRE_SEOULPARK"."PM25" IS '초미세먼지( ㎍/m3)';

COMMENT ON COLUMN "PRE_SEOULPARK"."SBW_IN_NUM" IS '지하철 승차 승객수';

COMMENT ON COLUMN "PRE_SEOULPARK"."SBW_OUT_NUM" IS '지하철 하차 승객수';

COMMENT ON COLUMN "PRE_SEOULPARK"."EVENT_OX" IS '행사여부(0/1)';

COMMENT ON COLUMN "PRE_SEOULPARK"."NAVI_SRC_NUM" IS '네비게이션 검색건수';

CREATE TABLE "PRE_CHILDPARK" (
	"PC_IDX"	int	GENERATED BY DEFAULT AS IDENTITY	NOT NULL,
	"STD_DATE"	date		NULL,
	"DAY"	int		NULL,
	"HOLIDAY_OX"	int		NULL,
	"ENT_NUM"	int		NULL,
	"HIGH_TEMP"	float		NULL,
	"LOW_TEMP"	float		NULL,
	"RAIN_AMOUNT"	float		NULL,
	"AVG_WIND"	float		NULL,
	"HIGH_WIND"	float		NULL,
	"PM10"	int		NULL,
	"PM25"	int		NULL,
	"SBW_IN_NUM"	int		NULL,
	"SBW_OUT_NUM"	int		NULL,
	"EVENT_OX"	int		NULL,
	"NAVI_SRC_NUM"	int		NULL
);

COMMENT ON COLUMN "PRE_CHILDPARK"."STD_DATE" IS '날짜(일별)';

COMMENT ON COLUMN "PRE_CHILDPARK"."DAY" IS '요일(월1 ~ 일7)';

COMMENT ON COLUMN "PRE_CHILDPARK"."HOLIDAY_OX" IS '공휴일여부(0/1)';

COMMENT ON COLUMN "PRE_CHILDPARK"."ENT_NUM" IS '총입장객수';

COMMENT ON COLUMN "PRE_CHILDPARK"."HIGH_TEMP" IS '최고기온';

COMMENT ON COLUMN "PRE_CHILDPARK"."LOW_TEMP" IS '최저기온';

COMMENT ON COLUMN "PRE_CHILDPARK"."RAIN_AMOUNT" IS '강수량(mm)';

COMMENT ON COLUMN "PRE_CHILDPARK"."AVG_WIND" IS '평균풍속(m/s)';

COMMENT ON COLUMN "PRE_CHILDPARK"."HIGH_WIND" IS '최대풍속(m/s)';

COMMENT ON COLUMN "PRE_CHILDPARK"."PM10" IS '미세먼지( ㎍/m3)';

COMMENT ON COLUMN "PRE_CHILDPARK"."PM25" IS '초미세먼지( ㎍/m3)';

COMMENT ON COLUMN "PRE_CHILDPARK"."SBW_IN_NUM" IS '지하철 승차 승객수';

COMMENT ON COLUMN "PRE_CHILDPARK"."SBW_OUT_NUM" IS '지하철 하차 승객수';

COMMENT ON COLUMN "PRE_CHILDPARK"."EVENT_OX" IS '행사여부(0/1)';

COMMENT ON COLUMN "PRE_CHILDPARK"."NAVI_SRC_NUM" IS '네비게이션 검색건수';


CREATE TABLE "LOTTE_EVER_ENTRANCE"(
    "LEE_IDX" INT GENERATED BY DEFAULT AS IDENTITY NOT NULL,
    "STD_DATE" VARCHAR(20) NULL,
    "EVER_ENT" INT NULL,
    "LOTTE_ENT" INT NULL,
    CONSTRAINT "PK_LOTTE_EVER_ENTRANCE" PRIMARY KEY(LEE_IDX)
);



ALTER TABLE "PRE_ENTRANCE" ADD CONSTRAINT "PK_PRE_ENTRANCE" PRIMARY KEY (
	"PE_IDX"
);

ALTER TABLE "PRE_HOLIDAY" ADD CONSTRAINT "PK_PRE_HOLIDAY" PRIMARY KEY (
	"PE_IDX"
);

ALTER TABLE "PRE_WEATHER" ADD CONSTRAINT "PK_PRE_WEATHER" PRIMARY KEY (
	"PW_IDX"
);

ALTER TABLE "PRE_THEMEPARK_EVENT" ADD CONSTRAINT "PK_PRE_THEMEPARK_EVENT" PRIMARY KEY (
	"PTE_IDX"
);

ALTER TABLE "PRE_SEOULPARK" ADD CONSTRAINT "PK_PRE_SEOULPARK" PRIMARY KEY (
	"PS_IDX"
);

ALTER TABLE "PRE_CHILDPARK" ADD CONSTRAINT "PK_PRE_CHILDPARK" PRIMARY KEY (
	"PC_IDX"
);

