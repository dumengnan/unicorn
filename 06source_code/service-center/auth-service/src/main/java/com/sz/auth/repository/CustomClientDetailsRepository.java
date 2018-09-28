package com.sz.auth.repository;


import com.sz.auth.domain.CustomClientDetails;
import org.springframework.data.repository.CrudRepository;

public interface CustomClientDetailsRepository extends CrudRepository<CustomClientDetails, String> {
    CustomClientDetails findByClientId(String clientId);
}
