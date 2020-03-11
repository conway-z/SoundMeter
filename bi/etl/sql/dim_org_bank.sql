insert into dim_org_bank
select  
		 m.org_id,  				-- 银行ID
		 m.org_simple_name, -- 银行简称
		 m.organization_name, -- 银行名称
		 COALESCE(h.bank_name_short_deal, headqt_bank_name_simple) as headqt_short_name, -- 总行简称（报表展示名称）
		-- COALESCE(h.bank_name_short, headqt_bank_name_simple) as headqt_short_name, -- 总行简称（报表展示名称,）
		m.par_org_id, -- 上级机构id
		m.par_org_name, -- 上级机构名称
		m.par_simple_name, -- 上级机构简称
		case when m.org_city != '' and m.org_city is not null then m.org_city
			when b.city is not null then trim(b.city)
			when bs.city is not null then trim(bs.city)
			else m.org_city
			end as city_name, -- 城市名称（报表展示名称，通过持证清单补全）
		 zorg_id,	-- 总行ID
		 headqt_bank_name, --  总行名称（与系统一致）
	   headqt_bank_name_simple, --  总行简称（与系统一致）
		 		m.ancestors,
			m.org_address,
			m.org_province_id,
			m.org_province,
			m.org_city_id,
			m.org_city,
			m.org_area_id,
			m.org_area,
			m.org_virtual_flag,
			m.org_virtual_id,
			m.org_type_id,
		  m.org_type_no,
		  m.org_type_name,
		  m.org_type_level,
			m.org_sys_level,
			date_format(now(), '%%Y-%%m-%%d %%H:%%i:%%S') as etl_time -- 数据入库时间
from (
	select 
		CASE WHEN prt.org_id='8888' THEN sor.org_id
			ELSE prt.org_id 
			END AS zorg_id,
		CASE WHEN prt.org_id='8888' THEN sor.organization_name
			ELSE prt.organization_name 
			END AS headqt_bank_name,
	  CASE WHEN prt.org_id='8888' THEN sor.org_simple_name
			ELSE prt.org_simple_name 
			END AS headqt_bank_name_simple,
		fa.org_id as par_org_id, -- 上级机构id
		fa.organization_name as par_org_name, -- 上级机构名称
		fa.org_simple_name as par_simple_name, -- 上级机构简称
		sor.ancestors,
		sor.org_id,
		sor.org_address,
		sor.org_simple_name,
		sor.organization_name,
		sor.org_province_id,
		sor.org_province,
		sor.org_city_id,
		sor.org_city,
		sor.org_area_id,
		sor.org_area,
		sor.org_virtual_flag,
		sor.org_virtual_id,
		sor.org_type_id,
		ty.org_type_no,
		ty.org_type_name,
		ty.org_type_level,
		length(sor.ancestors) - length(REPLACE (sor.ancestors, ',', '')) as org_sys_level
from sys_organization sor
left join sys_organization prt
	ON SUBSTRING_INDEX(SUBSTRING_INDEX(sor.ancestors,',',4),',',-1)=prt.org_id
left join sys_organization fa
	on sor.parent_id = fa.org_id
left join sys_organization_type ty
	on sor.org_type_id = ty.id
where sor.del_flag=0 and sor.org_id not in (6666,8888,9541) AND sor.org_type_id between 1008 and 1017
) m 
left join dim_org_bank_headqt_deal h on m.zorg_id = h.headqt_org_id and h.headqt_org_id is not null
left join ybj_bank_list  b on b.bank_name =  m.organization_name -- trim(replace(m.organization_name,char(10),''))  
	 and b.city != '浙江' 
	 and b.city is not null 
	 and b.bank_name !='中国农业银行股份有限公司湖州白鱼潭支行'  
left join ybj_bank_list  bs on bs.bank_name_abb =  m.org_simple_name 
	 and bs.bank_name_abb like '%%支行%%'
	 and bs.city != '浙江' 
	 and bs.city is not null 
	 and bs.bank_name !='中国农业银行股份有限公司湖州白鱼潭支行'  -- or b.bank_name_abb =  
;